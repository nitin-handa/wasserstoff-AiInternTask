
def determine_length(num_pages):
    # Determine the document length category based on the number of pages.
    if num_pages <= 10:
        return 'short'
    elif 10 < num_pages <= 30:
        return 'medium'
    else:
        return 'long'
