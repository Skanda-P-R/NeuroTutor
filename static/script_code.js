const codeEditor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
    mode: 'python',
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
        const response = await fetch('/check_errors', {
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

document.getElementById('correct-code').addEventListener('click', async () => {
    const code = codeEditor.getValue();
    const correctedOutput = document.getElementById('corrected-output');
    correctedOutput.textContent = 'Generating corrected code...';

    try {
        const response = await fetch('/correct_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code: code,
                errors: currentErrors.join("\n")
            }),
        });

        const data = await response.json();

        if (data.error) {
            correctedOutput.textContent = data.error;
        } else {
            if (data.corrected_code) {
                const match = data.corrected_code.match(/```(?:python)?\s*([\s\S]*?)```/i);
                const rawCode = match ? match[1].trim() : '';
                const explanation = data.corrected_code.replace(/```(?:python)?[\s\S]*?```/i, '').trim();
                const escapedCode = rawCode
                    .replace(/&/g, "&amp;")
                    .replace(/</g, "&lt;")
                    .replace(/>/g, "&gt;");

                correctedOutput.innerHTML = `
                <p>Here's the corrected code:</p>
                <textarea id="corrected-code-editor">${escapedCode}</textarea>
                <p><strong>Explanation:</strong></p>
                <p>${explanation.replace(/\n/g, '<br>')}</p>
            `;

                document.querySelector('.tab[data-tab="corrected"]').click();

                setTimeout(() => {
                    const editor = CodeMirror.fromTextArea(
                        document.getElementById('corrected-code-editor'), {
                        value: rawCode,
                        mode: 'python',
                        theme: 'default', // or 'monokai'
                        lineNumbers: true,
                        readOnly: true,
                        tabSize: 4,
                        indentUnit: 4,
                        viewportMargin: Infinity,
                        autoRefresh: true
                    });
                    const lineCount = editor.lineCount();
                    const lineHeight = 20;
                    editor.setSize(null, `${lineCount * lineHeight + 10}px`);
                }, 0);
            } else {
                correctedOutput.textContent = 'No corrections needed.';
            }
        }
        document.querySelector('.tab[data-tab="corrected"]').click();
    } catch (error) {
        correctedOutput.textContent = `Error: ${error.message}`;
    }
});