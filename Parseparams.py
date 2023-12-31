import re


class Parseparams:

    def parse_parameters(input_string):
        pattern = re.compile(r'(\w+)\s*=\s*(\[[^\]]*\]|"[^"]*"|\S+)')
        matches = pattern.findall(input_string)

        params_dict = {}
        for key, value in matches:
            # Handling string values without using ast.literal_eval
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]  # Remove double quotes
            elif value.startswith('[') and value.endswith(']'):
                # Handling list values
                value = [item.strip() for item in value[1:-1].split(',')]

            elif value.lower() == 'true':
                value = "true"
            elif value.lower() == 'false':
                value = "true"
            elif value == 'true,':
                value = "true"
            elif value == 'false,':
                value = "false"
            else:
                try:
                    # Attempt to convert to integer or float
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass  # Leave value as string if conversion fails

            params_dict[key] = value

        return params_dict

#If we are running from the command line, run the main function to test
if __name__ == "__main__":

    test_on = "verbal_utterance=\"I\'ve given you a receipt. Now, let's find the wallet to pay for your items.\", nonverbal_behavior=[nodding encouragingly], ready_to_continue=false, current_step=4)"
    print(Parseparams.parse_parameters(test_on))
