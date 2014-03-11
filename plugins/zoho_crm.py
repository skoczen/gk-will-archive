import requests, json
from will.settings import WILL_ZOHO_CRM_TOKEN
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
from string import split, join, lower


class ZohoCRMPlugin(WillPlugin):
    @route("/create-zoho-lead/")
    def create_lead(self):
        full_name = self.request.query.full_name
        phone = self.request.query.phone
        email = self.request.query.email
        business_name = self.request.query.business_name

        # TODO: remove this! :)
        full_name = "Levi C. Thomason"
        phone = "2086994042"
        email = "me@levithomason.com"
        business_name = "Thomason Industries"

        first_name = get_first_name(full_name)
        last_name = get_last_name(full_name)

        lead = {
            "First Name": first_name,
            "Last Name": last_name,
            "Phone": phone,
            "Email": email,
            "Company": business_name
        }

    @respond_to("^search zoho (?P<module>.*) for (?P<query>.*)")
    def search(self, message, module, query):
        self.say("Alright, I'm on it...")

        accounts_words = ['accounts', 'businesses', 'companies']
        contacts_words = ['contacts', 'people']
        module = lower(module)
        last_name = None

        if module in accounts_words:
            module = 'Accounts'
            return_fields = ['Account Name', 'Phone', 'Company Site']

        elif module in contacts_words:
            module = 'Contacts'
            return_fields = ['First Name', 'Last Name', 'Phone', 'Email']

            if len(split(query, ' ')) > 1:
                first_name = get_first_name(query)
                last_name = get_last_name(query)
                query = first_name

        else:
            self.say("I don't know of any '%s' module in Zoho" % module)
            return None

        record_ids = self.get_search_records(module, return_fields, query)

        results = []
        for record_id in record_ids:
            record = self.get_record_by_id(record_id, module, return_fields)

            record_fields = []
            ignore_fields = ['ACCOUNTID', 'CONTACTID']
            skip_record = False

            for field in record:
                for field_label in field:
                    field_value = field[field_label]

                    if field_label not in ignore_fields:
                        record_fields.append(field_value)

                        if field_label == 'Last Name' and last_name is not None:
                            if not lower(last_name) in lower(field_value):
                                skip_record = True

            if not skip_record:
                result = join(record_fields, ', ')
                results.append(result)

        search = {
            'results': results,
            'module': module,
            'query': query,
            'count': len(results)
        }
        results_html = rendered_template("zoho_search_results.html", search)
        self.say(results_html, html=True)

        return search

    @staticmethod
    def get_search_records(module, fields, query):
        '''
        Returns a list of record ids ['1234', '5678']
        '''

        response = zoho_api_request(module=module, api_method='getSearchRecords', query=query, fields=fields)
        has_results = response.get('result', None)

        results = []
        if has_results is not None:
            response_results = response['result'][module]['row']
            if isinstance(response_results, list):
                for row in response_results:
                    result_id = row['FL'][0]['content']
                    results.append("%s" % result_id)

            elif isinstance(response_results, dict):
                result_id = response_results['FL'][0]['content']
                results.append("%s" % result_id)
        else:
            pass

        return results

    def get_record_by_id(self, record_id, module, fields):
        '''
        Returns a list of dictionaries containing specified fields [{'label': value}, {'label': value}]
        '''
        response = zoho_api_request(module=module, api_method='getRecordById', record_id=record_id, fields=fields)
        has_results = response.get('result', None)

        record = []
        if has_results is not None:
            response_fields = response['result'][module]['row']['FL']

            if isinstance(response_fields, list):
                for field in response_fields:
                    field_value = field['content']
                    field_label = field['val']
                    field_dict = {field_label: field_value}

                    record.append(field_dict)

            elif isinstance(response_fields, dict):
                field_value = response_fields['content']
                field_label = response_fields['val']
                field_dict = {field_label: field_value}

                record.append(field_dict)

            else:
                pass

            return record


def zoho_api_request(module, api_method, query=None, record_id=None, fields=None):
    url = "https://crm.zoho.com/crm/private/json/%s/%s" % (module, api_method)

    params = {
        'authtoken': WILL_ZOHO_CRM_TOKEN,
        'url': url,
        'scope': 'crmapi',
        'newFormat': 1,
    }

    if record_id is not None:
        params['id'] = record_id

    if fields:
        select_columns = '%s(%s)' % (module, join(fields, ','))
        params['selectColumns'] = select_columns

        if query:
            search_condition = '(%s|contains|*%s*)' % (fields[0], query)
            params['searchCondition'] = search_condition

    request = requests.get(url, params=params)
    response_json = json.loads(request.text)
    response = response_json['response']

    return response


def get_first_name(full_name):
    names = split(full_name, ' ')
    first_name = names[0]

    return first_name


def get_last_name(full_name):
    names = split(full_name, ' ')
    last_name = names[len(names) - 1]

    return last_name
