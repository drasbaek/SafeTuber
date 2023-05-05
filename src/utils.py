""" utils.py
Author: 
    Anton Drasbæk Schiønning (202008161), GitHub: @drasbaek

Desc:
    Provides utility functions for the SafeTuber pipeline.
    It is concerned with functions for cleaning and processing the transcripts.
"""

def remove_long_chunks(text_chunks):
    '''
    This function removes chunks that are too long.
    Circumvents an issue with Whisper transcriptions where word / phrases often are repeated many times in the same chunk.

    Args:
        text_chunks (list): list of text chunks
    
    Returns:
        new_text_chunks (list): list of text chunks without chunks that are too long

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
    '''
    This function removes duplicate chunks.
    Circumvents issue with Whisper transcriptions where repeat chunks occur by fault.

    Args:
        text_chunks (list): list of text chunks
    
    Returns:
        new_text_chunks (list): list of text chunks without duplicate chunks

    '''

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
    '''
    This function removes concatenate chunks.
    Some chunks based on timestampts are short, uncompleted sentences.
    This function concatenates these based on the following rules:
        1. If the current string is shorter than 10 words, it is concatenated with the next string.
        2. If the current string does not end in a period, it is concatenated with the next string.
        3. If the current string is longer than 10 words and ends in a period, it is added to the list of joined chunks.
    
    This achieves a more natural language flow in the final transcript.

    Args:
        text_chunks (list): list of text chunks
    
    Returns:
        joined_chunks (list): list of text chunks with concatenated chunks

    '''
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
    '''
    Combines the above functions to clean the text chunks in single pipeline.

    Args:
        text_chunks (list): list of unprocessed text chunks
    
    Returns:
        text_chunks_processed (list): list of processed text chunks
        
    '''

    # remove long chunks
    text_chunks = remove_long_chunks(text_chunks)

    # remove duplicates
    text_chunks_no_dup = remove_duplicates(text_chunks)

    # concatenate chunks
    text_chunks_processed = concatenate_chunks(text_chunks_no_dup)

    return text_chunks_processed