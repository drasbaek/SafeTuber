# Desc: Utility functions for the project
'''

'''
def remove_long_chunks(text_chunks):
    '''
    Removes long chunks as most of these will be due to an error where a word is repeated often in the audio transcription
    '''
    # initialize new list
    new_text_chunks = []

    # loop through chunks
    for text in text_chunks:

        # if text is too long, skip
        if len(text.split()) > 25:
            continue

        # else add to new list
        else:
            new_text_chunks.append(text)

    return new_text_chunks


def remove_duplicates(text_chunks):
    # initialize new list
    new_text_chunks = []

    # initialize previous text
    prev_text = ""

    # loop through chunks
    for text in text_chunks:

        # if text is the same as previous text, skip
        if text == prev_text:
            continue

        # else add to new list
        else:
            new_text_chunks.append(text)
            prev_text = text

    return new_text_chunks

def concatenate_chunks(text_chunks):
    joined_chunks = []
    current_string = ""

    for i, string in enumerate(text_chunks):
        
        # Join current string with next string if current string is too short or it doesn't end in a period
        if len(current_string.split()) < 10:
            current_string += " " + string

        elif current_string[-1] != ".":
            current_string += " " + string
        
        # Add current string to joined data if it's long enough
        else:
            joined_chunks.append(current_string.strip())
            current_string = string

        # Add the last string to the joined data
        if i == len(text_chunks) - 1:
            joined_chunks.append(current_string.strip())
    
    return joined_chunks


def clean_text(text_chunks):
    # remove long chunks
    text_chunks = remove_long_chunks(text_chunks)

    # remove duplicates
    text_chunk_no_dup = remove_duplicates(text_chunks)

    # concatenate chunks
    text_chunks_concat = concatenate_chunks(text_chunk_no_dup)

    return text_chunks_concat