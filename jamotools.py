import re


def break_down_syllable_block(syllable_block):
    # Break down a Korean syllable block into its constituent jamo characters
    # and return them as a list
    pattern = re.compile("[가-힣]")  # Match Korean syllable blocks only
    if not pattern.match(syllable_block):
        return None  # Input is not a valid Korean syllable block
    # Calculate Unicode offset of syllable block
    offset = ord(syllable_block) - 0xAC00
    # Find Unicode character for lead consonant
    lead_consonant = chr((offset // 28) // 21 + 0x1100)
    # Find Unicode character for vowel
    vowel = chr((offset // 28) % 21 + 0x1161)
    trail_consonant = None
    if offset % 28 > 0:
        # Find Unicode character for trail consonant, if it exists
        trail_consonant = chr((offset % 28) + 0x11A7)
    return [lead_consonant, vowel, trail_consonant] if trail_consonant else [lead_consonant, vowel]

# Write the opposite of the function break_down_syllable_block(syllable_block)


def create_syllable_block(jamo_list):
    # Create a Korean syllable block from a list of jamo characters
    # and return it as a string
    if len(jamo_list) == 2:
        # Calculate Unicode offset of syllable block
        offset = (ord(jamo_list[0]) - 0x1100) * 588 + \
            (ord(jamo_list[1]) - 0x1161) * 28
        # Find Unicode character for syllable block
        syllable_block = chr(offset + 0xAC00)
        return syllable_block
    elif len(jamo_list) == 3:
        # Calculate Unicode offset of syllable block
        offset = (ord(jamo_list[0]) - 0x1100) * 588 + \
            (ord(jamo_list[1]) - 0x1161) * 28 + (ord(jamo_list[2]) - 0x11A7)
        # Find Unicode character for syllable block
        syllable_block = chr(offset + 0xAC00)
        return syllable_block
    else:
        return None  # Input is not a valid list of jamo characters


def get_formatted_string(s, n):
    # Split the input string into Korean syllable blocks using regex
    # pattern = re.compile("[가-힣]+")
    # syllables = pattern.findall(s)

    # Break down each syllable into its constituent jamo characters
    """
    jamo_list = []
    for syllable in syllables:
        for jamo in syllable:
            jamo_list.append(jamo)
    """
    # print(jamo_list)
    jamo_list = break_down_syllable_block(s)
    print(jamo_list)
    # Combine the first n jamo characters into new syllable blocks
    new_syllables = []
    current_syllable = ""
    for i in range(n):
        if i >= len(jamo_list):
            break
        current_syllable += jamo_list[i]
    new_syllables.append(current_syllable)

    # Format the new syllable blocks into a properly formatted Korean string
    new_string = ""
    for syllable in new_syllables:
        lead = ord(syllable[0]) - 0xac00
        lead_consonant = chr((lead // 28) // 21 + 0x1100)
        vowel = chr((lead // 28) % 21 + 0x1161)
        if len(syllable) == 3:
            trail = ord(syllable[2]) - 0xac00
            trail_consonant = chr((trail % 28) + 0x11a7)
            new_string += lead_consonant + vowel + trail_consonant
        else:
            new_string += lead_consonant + vowel

    return new_string


def is_jongseong(jamo):
    """Returns True if the given jamo character is a valid Jongseong."""
    codepoint = ord(jamo)
    return 0x3131 <= codepoint <= 0x314e or 0x3165 <= codepoint <= 0x3186


def is_jungseong(jamo):
    """Returns True if the given jamo character is a valid Jungseong."""
    codepoint = ord(jamo)
    return 0x314f <= codepoint <= 0x3163 or 0x3187 <= codepoint <= 0x318e


def is_chosung(jamo):
    """Returns True if the given jamo character is a valid Chosung."""
    codepoint = ord(jamo)
    return 0x1100 <= codepoint <= 0x1112 or 0x3131 <= codepoint <= 0x314e


def jamo_to_syllables(jamo_list):
    # Initialize variables
    syllables = []
    current_syllable = ""

    # Iterate through the jamo list and combine them into syllable blocks
    for jamo in jamo_list:
        # Check if the current jamo completes a syllable block
        if len(current_syllable) == 2 and is_jongseong(jamo):
            # Add the trailing consonant to the current syllable block
            current_syllable += jamo
            syllables.append(current_syllable)
            current_syllable = ""
        elif len(current_syllable) == 1 and is_jungseong(jamo):
            # Add the vowel to the current syllable block
            current_syllable += jamo
            syllables.append(current_syllable)
            current_syllable = ""
        elif len(current_syllable) == 0 and is_chosung(jamo):
            # Add the leading consonant to a new syllable block
            current_syllable += jamo
        else:
            # Invalid combination of jamo letters, reset current syllable block
            current_syllable = ""

    # Check if there are any remaining jamo letters in the current syllable block
    if len(current_syllable) > 0:
        syllables.append(current_syllable)

    # Combine the syllable blocks into a single string
    print(syllables)
    return "".join(syllables)


def string_to_block_list(hangeul_string):
    syllable_block_list = []
    for block in hangeul_string:
        syllable_block_list.append(block)
    return syllable_block_list


def block_list_to_jamo_list(syllable_block_list):
    jamo_list = []
    for block in syllable_block_list:
        jamo_list += break_down_syllable_block(block)
    return jamo_list


# Converts a list of jamo characters to a Hangeul syllable block
# Parameter: jamo_list, a list of jamo characters
# Return: a character of the syllable block
def jamo_list_to_block(jamo_list):
    return jamo_to_syllables(jamo_list)


def jamo_list_to_string(jamo_list):
    out_string = ""
    for jamo in jamo_list:
        out_string += jamo
    return out_string


def delete_jamo(jamo_list, n):
    return jamo_list[:-n]


def n_jamo_to_string(jamo_list, n):
    out_string = ""
    for jamo in jamo_list[:n]:
        out_string += jamo
    return out_string


if __name__ == "__main__":
    # s = "안녕하세요"
    # n = 6
    # print(get_formatted_string(s, n))
    hangeul_string = "안녕하세요"
    # block_list = []
    # for block in string:
    #    block_list.append(block)

    syllable_block_list = string_to_block_list(hangeul_string)

    # syllable_block = "한"
    # full_jamo_list = []
    # for block in block_list:
    #    block_jamo_list = break_down_syllable_block(block)
    #    full_jamo_list += block_jamo_list

    full_jamo_list = block_list_to_jamo_list(syllable_block_list)
    print(full_jamo_list)

    # out_string = ""
    # for jamo in full_jamo_list:
    #    out_string += jamo

    out_string = jamo_list_to_string(full_jamo_list)
    print(out_string)

    # out_string2 = ""
    # for i in range(3):
    #    out_string2 += full_jamo_list[i]
    out_string2 = n_jamo_to_string(full_jamo_list, 3)
    print(out_string2)
    # encoded = out_string3.encode("utf-8")
    # temp = []
    # temp

    new_jamo_list = delete_jamo(full_jamo_list, 7)
    out_string3 = jamo_list_to_string(new_jamo_list)
    print(out_string3)

    jamo_list3 = ['ㄱ', 'ㅏ', 'ㄴ']
    out_string4 = jamo_list_to_block(jamo_list3)
    print(out_string4)

    # s = "안녕하세요"
    # encoded = s.encode("utf-8")
    # print(encoded)

    # jamo_list = ['ㅎ', 'ㅏ', 'ㄴ']
    # syllable_block = jamo_list_to_block(jamo_list)
    # print(syllable_block)

# valid_syllable_str = jamo_to_syllables(full_jamo_list)
# print(valid_syllable_str)

"""
    # --------------------------------------------------------------#

    # Combine the first n jamo characters into new syllable blocks
    n = 5
    new_syllables = []
    current_syllable = ""
    for i in range(n):
        if i >= len(full_jamo_list):
            break
        current_syllable += full_jamo_list[i]
    new_syllables.append(current_syllable)

    # Format the new syllable blocks into a properly formatted Korean string
    new_string = ""
    for syllable in new_syllables:
        lead = ord(syllable[0]) - 0xac00
        lead_consonant = chr((lead // 28) // 21 + 0x1100)
        vowel = chr((lead // 28) % 21 + 0x1161)
        if len(syllable) == 3:
            trail = ord(syllable[2]) - 0xac00
            trail_consonant = chr((trail % 28) + 0x11a7)
            new_string += lead_consonant + vowel + trail_consonant
        else:
            new_string += lead_consonant + vowel

    print(new_string)
"""
# s2 = "반"
# n2 = 3
# print(get_formatted_string(s2, n2))
