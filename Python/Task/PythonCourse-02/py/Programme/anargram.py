def check_anagram(text1, text2):
    # Remove spaces and convert to lowercase for comparison
    text1 = text1.replace(" ", "").lower()
    text2 = text2.replace(" ", "").lower()

    # Check if the sorted characters of both strings are equal
    return sorted(text1) == sorted(text2)

# Test the function
result = check_anagram("listen", "silent")
print("Are 'liste' and 'silent' anagrams?", result)
