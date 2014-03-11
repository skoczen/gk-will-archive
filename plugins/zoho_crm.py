import requests, json
from will.settings import WILL_ZOHO_CRM_TOKEN
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
from string import split, join


class ZohoCRMPlugin(WillPlugin):

    @staticmethod
    def get_first_name(full_name):
        names = split(full_name, ' ')
        first_name = names[0]

        return first_name

    @staticmethod
    def get_last_name(full_name):
        names = split(full_name, ' ')
        last_name = names[len(names)-1]

        return last_name

    @route("/create-zoho-lead/")
    def create_lead(self):
        full_name = "Levi C. Thomason"
        phone = "2086994042"
        email = "me@levithomason.com"
        business_name = "Thomason Industries"

        first_name = self.get_first_name(full_name)
        last_name = self.get_last_name(full_name)

        lead = {
            "First Name": first_name,
            "Last Name": last_name,
            "Phone": phone,
            "Email": email,
            "Company": business_name
        }

    @respond_to("^search zoho (companies|businesses|accounts) for (?P<account>.*)")
    def search_account(self, message, account):

        search = self.get_search_records('Accounts', 'Accounts(Account Name)', account)

        if search is None:
            search = dict(module='Accounts', query=account)

        results_html = rendered_template("zoho_search_results.html", search)

        self.say(results_html, html=True)

        return search

    @respond_to("^search zoho contacts for (?P<contact>.*)")
    def search_contact(self, message, contact):

        search = self.get_search_records('Contacts', 'Contacts(First Name)', contact)

        context = {
            "module": 'Accounts',
            "query": contact
        }

        context += search

        results_html = rendered_template("zoho_search_results.html", context)

        self.say(results_html, html=True)

        return search

    def get_search_records(self, module, select_columns, query):
        url = "https://crm.zoho.com/crm/private/json/%s/getSearchRecords" % module

        if module == 'Accounts':
            search_condition = "(Account Name|contains|*%s*)" % query

        if module == 'Contacts':
            if len(split(query, ' ')) > 1:
                first_name = self.get_first_name(query)
                search_condition = "(First Name|contains|*%s*)" % first_name
            else:
                search_condition = "(First Name|contains|*%s*)" % query

        params = {
            'authtoken': WILL_ZOHO_CRM_TOKEN,
            'scope': 'crmapi',
            'newFormat': 1,
            'selectColumns': select_columns,
            'searchCondition': search_condition,
        }

        request = requests.get(url, params=params)
        response_json = json.loads(request.text)
        response = response_json['response']

        if response.get('nodata', None) is not None:
            return None

        else:
            try:
                response_results = response['result'][module]['row']

                results = []
                if isinstance(response_results, list):
                    for row in response_results:
                        account_name = row['FL'][1]['content']
                        results.append("%s" % account_name)

                elif isinstance(response_results, dict):
                    account_name = response_results['FL'][1]['content']
                    results.append("%s" % account_name)

                search = {
                    "results": results,
                    "count": len(results)
                }

                return search

            except KeyError:
                self.say("I'm not sure how to handle this data structure:\n\n%s" % json.dumps(response))
