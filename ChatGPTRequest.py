import csv
import openai
import time
import multiprocessing
from openai import ChatCompletion

with open("key.txt") as f:
    openai.api_key = f.read().strip()

# Read the CSV file with proper encoding
with open('input.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)

# Function to process a single row
def process_row(row, index):
    if index == 1:
        # Skip the header row
        return None

    prompt = row[0].strip()

    try:
        # Create the response
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        time.sleep(2)  # Pause for 2 seconds to avoid rate limiting

        # Extract the generated response
        generated_response = response['choices'][0]['message']['content']

        # Create a new row with the prompt and generated response
        new_row = {
            'Prompt': prompt,
            'Response': generated_response
        }

        print(f"#{index}: Generated response for prompt: {prompt}")

        return new_row

    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors
        error_message = str(e)
        new_row = {
            'Prompt': prompt,
            'Response': f"OpenAI API Error: {error_message}"
        }

        print(f"#{index}: Error for prompt: {prompt} - OpenAI API Error: {error_message}")

        return new_row

    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        new_row = {
            'Prompt': prompt,
            'Response': f"Error: {error_message}"
        }

        print(f"#{index}: Error for prompt: {prompt} - Error: {error_message}")

        return new_row

if __name__ == '__main__':
    # Create a multiprocessing Pool
    pool = multiprocessing.Pool()

    # Process each row in parallel and collect the results
    results = [pool.apply_async(process_row, (row, index)) for index, row in enumerate(rows[1:], 2)]
    updated_rows = [res.get() for res in results if res.get() is not None]  # Exclude None values

    # Close the multiprocessing Pool
    pool.close()
    pool.join()

    # Write the updated rows to the CSV file with proper encoding
    fieldnames = ['Prompt', 'Response']  # Set the desired fieldnames for the CSV file
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print("Responses written to CSV file.")
