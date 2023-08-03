import csv
import boto3

def get_data_by_region_bldg_date(data, region, bldg, date=None):
    new_bldg = bldg.title().replace(' ', '_')  # Convert building type to title case and replace spaces with underscores
    new_region = region.upper().replace(' ', '_')  # Convert region to upper case and replace spaces with underscores

    feature = f'PRED_{new_bldg}_Benchmark_SA_{new_region}'

    try:
        return data[feature]
    except KeyError:
        print(f"Feature: '{feature}' not found in data.")
        return None

def lambda_handler(event, context):
    # Check if the user_region slot is populated
    if 'user_region' in event['currentIntent']['slots']:
        user_region = event['currentIntent']['slots']['user_region']
    else:
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Invalid event structure. Missing user_region slot.'
                }
            }
        }

    # Check if the user_house_type slot is populated
    if 'user_house_type' in event['currentIntent']['slots']:
        user_house_type = event['currentIntent']['slots']['user_house_type']
    else:
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Invalid event structure. Missing user_house_type slot.'
                }
            }
        }

    # Check if the user_date slot is populated
    if 'user_date' in event['currentIntent']['slots']:
        user_date = event['currentIntent']['slots']['user_date']
    else:
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Invalid event structure. Missing user_date slot.'
                }
            }
        }

    # Define the S3 bucket and file name
    bucket_name = 'project2fintech2023'
    file_name = 'total_chart_regional_save.csv'

    # Create an S3 client
    s3 = boto3.client('s3')

    try:
        # Get the CSV file from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        csv_data = response['Body'].read().decode('utf-8').splitlines()

        # Read the CSV data
        reader = csv.reader(csv_data)
        next(reader)  # Skip the header row

        # Find the matching row based on date and region/building type
        matching_row = None
        for row in reader:
            csv_date = row[0]
            if csv_date == user_date:
                matching_row = row
                break

        if matching_row is not None:
            building_type = user_house_type.lower()

            # Get the predicted composite benchmark based on region and building type
            data = {col: val for col, val in zip(csv_data[0].split(','), matching_row)}
            predicted_price = get_data_by_region_bldg_date(data, user_region, building_type)

            if predicted_price is not None:
                formatted_price = ' ${:,.2f} CAD'.format(float(predicted_price))

                return {
                    'dialogAction': {
                        'type': 'Close',
                        'fulfillmentState': 'Fulfilled',
                        'message': {
                            'contentType': 'PlainText',
                            'content': f"The predicted price for a {building_type} in {user_region.title()} during {user_date} is {formatted_price}."
                        }
                    }
                }
            else:
                return {
                    'dialogAction': {
                        'type': 'Close',
                        'fulfillmentState': 'Failed',
                        'message': {
                            'contentType': 'PlainText',
                            'content': f"No data found for the specified region '{user_region}' or building type '{building_type}'."
                        }
                    }
                }
        else:
            return {
                'dialogAction': {
                    'type': 'Close',
                    'fulfillmentState': 'Failed',
                    'message': {
                        'contentType': 'PlainText',
                        'content': f"No data found for the specified date '{user_date}'."
                    }
                }
            }

    except Exception as e:
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': f"Error retrieving the CSV file: {str(e)}"
                }
            }
        }