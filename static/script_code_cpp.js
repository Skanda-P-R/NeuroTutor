const codeEditor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
    mode: 'text/x-c++src',
    theme: 'default',
    lineNumbers: true,
    indentUnit: 4,
    tabSize: 4,
    indentWithTabs: false,
    autoCloseBrackets: true,
    matchBrackets: true,
    lint: true
});

let currentErrors = [];

document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        const tabName = tab.getAttribute('data-tab');
        document.getElementById(`${tabName}-content`).classList.add('active');
    });
});

document.getElementById('check-errors').addEventListener('click', async () => {
    const code = codeEditor.getValue();
    const errorsOutput = document.getElementById('errors-output');
    errorsOutput.textContent = 'Checking for errors...';
    try {
        const response = await fetch('/check_errors_cpp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code }),
        });

        const data = await response.json();
        currentErrors = data.errors || [];

        if (currentErrors.length === 0) {
            errorsOutput.textContent = 'No errors found!';
        } else {
            errorsOutput.innerHTML = marked.parse(currentErrors.join("\n"));
        }
        document.querySelector('.tab[data-tab="errors"]').click();
    } catch (error) {
        errorsOutput.textContent = `Error: ${error.message}`;
    }
});

document.getElementById('upload-image').addEventListener('change', async (event) => {
    const file = event.target.files[0];
    const status = document.getElementById('ocr-status');
    if (!file) return;

    status.textContent = 'Reading image and extracting text...';

    try {
        const { data: { text } } = await Tesseract.recognize(file, 'eng', {
            logger: m => {
                if (m.status === 'recognizing text') {
                    status.textContent = `Processing: ${Math.round(m.progress * 100)}%`;
                }
            }
        });

        status.textContent = 'Extraction complete!';
        codeEditor.setValue(text.trim());
    } catch (error) {
        status.textContent = `OCR failed: ${error.message}`;
    }
});