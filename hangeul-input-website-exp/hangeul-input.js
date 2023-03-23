function decomposeSyllable(syllable) {
    const syllableCode = syllable.charCodeAt(0) - 0xAC00;
    const choseong = Math.floor(syllableCode / 588);
    const jungseong = Math.floor((syllableCode - (588 * choseong)) / 28);
    const jongseong = syllableCode % 28;

    return { choseong, jungseong, jongseong };
}

function composeSyllable(choseong, jungseong, jongseong = 0) {
    return String.fromCharCode(0xAC00 + (588 * choseong) + (28 * jungseong) + jongseong);
}

function handleBackspace(event) {
    const textarea = document.getElementById('korean-textarea');

    if (event.key === 'Backspace') {
        const cursorPosition = textarea.selectionStart;
        const prevChar = textarea.value.charAt(cursorPosition - 1);
        const prevCharCode = prevChar.charCodeAt(0);

        if (0xAC00 <= prevCharCode && prevCharCode <= 0xD7A3) {
            event.preventDefault();

            const { choseong, jungseong, jongseong } = decomposeSyllable(prevChar);

            // If the syllable has a jongseong, remove it
            if (jongseong > 0) {
                const newChar = composeSyllable(choseong, jungseong);
                textarea.value = textarea.value.substring(0, cursorPosition - 1) + newChar + textarea.value.substring(cursorPosition);
                textarea.selectionStart = textarea.selectionEnd = cursorPosition;
            } 
            // If the syllable does not have a jongseong, remove the jungseong
            else if (jungseong > 0) {
                const newChar = composeSyllable(choseong);
                textarea.value = textarea.value.substring(0, cursorPosition - 1) + newChar + textarea.value.substring(cursorPosition);
                textarea.selectionStart = textarea.selectionEnd = cursorPosition - 1;
            }
            // If the syllable only has a choseong, remove it and replace it with the corresponding jamo
            else {
                const choseongTable = [
                    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
                ];
                textarea.value = textarea.value.substring(0, cursorPosition - 1) + choseongTable[choseong] + textarea.value.substring(cursorPosition);
                textarea.selectionStart = textarea.selectionEnd = cursorPosition; // Note to ChatGPT: I got rid of the "- 1" here because I don't want the cursor to jump to the start after a deletion, which it was doing 
            }
        }
    }
}

function handleInput(event) {
    const textarea = document.getElementById('korean-textarea');
    const cursorPosition = textarea.selectionStart;
    const prevChar = textarea.value.charAt(cursorPosition - 1);
    const prevCharCode = prevChar.charCodeAt(0);
    const typedChar = event.data;
    const typedCharCode = typedChar.charCodeAt(0);

    if (0xAC00 <= prevCharCode && prevCharCode <= 0xD7A3 && 0x3131 <= typedCharCode && typedCharCode <= 0x3163) {
        const { choseong, jungseong, jongseong } = decomposeSyllable(prevChar);

        if (jongseong === 0 && isJungseong(typedChar)) {
            event.preventDefault();
            const newJungseongIndex = jungseongTable.indexOf(typedChar);
            const newChar = composeSyllable(choseong, newJungseongIndex);
            textarea.value = textarea.value.substring(0, cursorPosition - 1) + newChar + textarea.value.substring(cursorPosition);
            textarea.selectionStart = textarea.selectionEnd = cursorPosition + 1;
        } else if (jongseong === 0 && isJongseong(typedChar)) {
            event.preventDefault();
            const newJongseongIndex = jongseongTable.indexOf(typedChar);
            const newChar = composeSyllable(choseong, jungseong, newJongseongIndex);
            textarea.value = textarea.value.substring(0, cursorPosition - 1) + newChar + textarea.value.substring(cursorPosition);
            textarea.selectionStart = textarea.selectionEnd = cursorPosition + 1;
        }
    }
}

function isJungseong(char) {
    return jungseongTable.includes(char);
}

function isJongseong(char) {
    return jongseongTable.includes(char);
}

const textarea = document.getElementById('korean-textarea');
textarea.addEventListener('input', handleInput);
textarea.addEventListener('keydown', handleBackspace);

