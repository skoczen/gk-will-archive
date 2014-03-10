import requests, json
from will import settings
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class ZohoCRMPlugin(WillPlugin):

    @respond_to("^zoho company$")
    def add_company(self, message):
        company_name = "ABC Company"
        phone = "123-456-7809"

        url = "https://crm.zoho.com/crm/private/json/Accounts/insertRecords"
        params = {
            'authtoken': settings.WILL_ZOHO_CRM_TOKEN,
            'scope': 'crmapi',
            'newFormat': 1,
            'xmlData': '<Accounts><row no="1"><FL val="Account Name">%s</FL><FL val="phone">%s</FL></row></Accounts>'
                       % (company_name, phone)
        }

        r = requests.get(url, params=params)

        if r.status_code == requests.codes.ok:
            self.reply(message, 'I added "%s" to Zoho CRM.' % company_name)

        self.reply(message, "Here's what I heard back: \n\n %s" % r.text)

    @respond_to("^zoho contact$")
    def add_contact(self, message):
        first_name = "Aaaaa"
        last_name = "Bbbbbbbb"
        phone = "123-456-7809"
        email = "test@test.com"
        company_name = "ABC Company"

        self.reply(message, "%s, %s, %s, %s, %s" % (first_name, last_name, phone, email, company_name))

    @route("/find-zoho-account/")
    @respond_to("^(find|search|look|lookup|look up|list|ls) (zoho|zoho for) (company|companies for|business|businesses for|account|accounts for) (?P<account>.*)")
    def find_account(self, message, account):

        self.say('/me goes looking for "%s"...' % account, message=message)

        url = "https://crm.zoho.com/crm/private/json/Accounts/getSearchRecords"
        params = {
            'authtoken': settings.WILL_ZOHO_CRM_TOKEN,
            'scope': 'crmapi',
            'newFormat': 1,
            'selectColumns': 'Accounts(Account Name)',
            'searchCondition': '(Account Name|contains|*%s*)' % account,
        }

        request = requests.get(url, params=params)
        response_json = json.loads(request.text)
        response = response_json['response']

        results = []

        try:
            self.say("Response is: " + str(type(response['result']['Accounts']['row'])))

            for row in response['result']['Accounts']['row']:
                account_name = row['FL'][1]['content']
                results.append("%s" % account_name)

        except KeyError:
            pass

        truncated = len(results) >= 20
        count = len(results)

        context = {
            "account": account,
            "results": results,
            "count": count,
            "truncated": truncated,
        }

        results_html = rendered_template("zoho/company_search_results.html", context)

        self.say(results_html, html=True)

        return results

    @route("/find-zoho-contact/")
    @respond_to("^(find|search|look|lookup|look up|list|ls) (zoho|zoho for) (contact|contacts for|contacts named) (?P<contact>.*)")
    def find_contact(self, message, contact):
        self.say('/me goes looking for "%s"...' % contact, message=message)

        url = "https://crm.zoho.com/crm/private/json/Contacts/getSearchRecords"
        params = {
            'authtoken': settings.WILL_ZOHO_CRM_TOKEN,
            'scope': 'crmapi',
            'newFormat': 1,
            'selectColumns': 'Contacts(Last Name)',
            'searchCondition': '(Last Name|contains|*%s*)' % contact,
        }

        request = requests.get(url, params=params)
        request_json = request.json()
        response = request_json['response']

        results = []

        self.say(str(len(response['result']['Contacts']['row'])))
        self.say(str(response))

        try:
            rows = []
            for row in response['result']['Contacts']['row']:
                rows.append(row)

            for row in rows:
                self.say(row['FL'])
                contact_name = row['FL'][1]['content']
                results.append("%s" % contact_name)

        except KeyError:
            pass

        truncated = len(results) >= 20
        count = len(results)

        context = {
            "contact": contact,
            "results": results,
            "count": count,
            "truncated": truncated,
        }

        results_html = rendered_template("zoho/contact_search_results.html", context)

        self.say(results_html, html=True)

        return results
