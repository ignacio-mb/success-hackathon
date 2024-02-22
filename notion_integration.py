# openai.api_key = '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'
# NOTION_API_KEY = 'secret_sDVD6QVlSxBEBEryvR8RGxM4kU5nJC95iTcweAFt1Dv'

import requests
import openai

openai.api_key = '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'
NOTION_API_KEY = 'secret_sDVD6QVlSxBEBEryvR8RGxM4kU5nJC95iTcweAFt1Dv'

def extract_toggle_content(block):
    """
    Extracts the content inside a toggle block.
    """
    content = ""
    for child_block in block.get('toggle', {}).get('content', []):
        if child_block['type'] == 'paragraph':
            paragraph_text = ''.join([text['plain_text'] for text in child_block.get('paragraph', {}).get('text', [])])
            content += paragraph_text + "\n"
        elif child_block['type'] == 'heading_1':
            heading_text = ''.join([text['plain_text'] for text in child_block.get('heading_1', {}).get('text', [])])
            content += heading_text + "\n"
        # Add more conditions for other block types as needed
    return content.strip()

def get_page_blocks(page_id):
    """
    Fetches all blocks of a Notion page using the Notion API with pagination.
    """
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13"
    }

    all_blocks = []
    next_cursor = None

    while True:
        params = {'start_cursor': next_cursor} if next_cursor else {}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        all_blocks.extend(data.get('results', []))

        if not data.get('has_more'):
            break

        next_cursor = data.get('next_cursor')

    return all_blocks

def preprocess_text(text):
    # Implement any preprocessing steps here
    return text

def display_content(blocks):
    if not blocks:
        print("No blocks found.")
        return
    
    # print("Page Content:")
    # try:
    #     for block in blocks:
    #         block_type = block['type']
            
    #         if block_type == 'paragraph':
    #             content = block.get('paragraph', {}).get('text', [])
    #             if content:
    #                 print(''.join([text['plain_text'] for text in content]))
    #             else:
    #                 print("No text content in this paragraph.")
            
    #         elif block_type == 'heading_1':
    #             content = block.get('heading_1', {}).get('text', [])
    #             if content:
    #                 print("**" + content[0]['plain_text'] + "**")
    #             else:
    #                 print("No text content in this heading.")
            
    #         elif block_type == 'heading_3':
    #             content = block.get('heading_3', {}).get('text', [])
    #             if content:
    #                 print("***" + content[0]['plain_text'] + "***")
    #             else:
    #                 print("No text content in this heading.")
            
    #         elif block_type == 'to_do':
    #             content = block.get('to_do', {}).get('text', [])
    #             if content:
    #                 print("- [{}] {}".format('x' if block['to_do']['checked'] else ' ', content[0]['plain_text']))
    #             else:
    #                 print("- [{}]".format('x' if block['to_do']['checked'] else ' '))
            
    #         elif block_type == 'bulleted_list_item':
    #             content = block.get('bulleted_list_item', {}).get('text', [])
    #             if content:
    #                 print("- " + content[0]['plain_text'])
    #             else:
    #                 print("No text content in this bullet list item.")
            
    #         elif block_type == 'toggle':
    #             toggle_content = extract_toggle_content(block.get('toggle', {}).get('children', []))
    #             if toggle_content:
    #                 print(toggle_content)
    #             else:
    #                 print("No content inside this toggle block.")
    # except KeyError:
    #     print("End of page parsing.")

if __name__ == '__main__':
    page_id = input("Enter the Notion page ID: ")
    print("Fetching page content...")
    blocks = get_page_blocks(page_id)
    display_content(blocks)

    # Extract meeting notes content
    meeting_notes_content = '\n'.join([text.get('plain_text', '') for block in blocks if block['type'] == 'paragraph' for text in block.get('paragraph', {}).get('text', [])])
    
    # Preprocess meeting notes content
    preprocessed_meeting_notes = preprocess_text(meeting_notes_content)
    


    # Construct prompt
    # prompt = f"I'm sending you meeting notes from a enterprise customer. Your goal is to transform and catalogue the relevant data into a table structure to then insert into a PostgreSQL database to create customer profiles based on the data from the meeting notes. I will also send the initial table structure, and then you will go adding columns if you find information that needs to be a column that is not created yet. \n\nMeeting Notes:\n{preprocessed_text}"
    # prompt = f"I'm sending you meeting notes from an enterprise customer. Your goal is to transform and catalogue the relevant data into a table structure to then insert into a PostgreSQL database to create customer profiles based on the data from the meeting notes. I will also send the initial table structure, and then you will go adding columns if you find information that needs to be a column that is not created yet. \n\nMeeting Notes:\n{preprocessed_meeting_notes}"
    
    prompt = f"I'm sending you meeting notes from an enterprise customer. Give me a paragraph describing the customer use case with the heading 'Use Case', another one with the main pain points with the heading 'Pain Points' and another with interests for future product features called 'Interests'.\n\nMeeting Notes:\n{preprocessed_meeting_notes}"

    print('\n')
    print('\n')
    print(f"BEING SENT TO OPEN AI: I'm sending you meeting notes from an enterprise customer. Give me a paragraph describing the customer use case with the heading 'Use Case', another one with the main pain points with the heading 'Pain Points' and another with interests for future product features called 'Interests'")
    
    # Send prompt to OpenAI for analysis
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You: "},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400
    )
    
    # Display OpenAI response
    response_text = response['choices'][0]['message']['content']
    print('\n')
    print('\n')
    print(f"OPENAI RESPONSE:", response_text.strip())
