const userId = document.body.dataset.userId;
console.log(userId)
const questionOutput = document.getElementById("question-output");
const submitButton = document.getElementById("submit-code");
const editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
    lineNumbers: true,
    mode: "python",
    theme: "default"
});

let currentQuestionId = null;
let currentQuestionText = null;
let currentConcept = null;

function fetchNextQuestion() {
    fetch("/get_next_question", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId })
    })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            if (data.question_text) {
                currentQuestionId = data.question_id;
                currentQuestionText = data.question_text;
                currentConcept = data.concept;
                questionOutput.textContent = data.question_text;
            } else {
                questionOutput.textContent = "🎉 All questions completed!";
                submitButton.disabled = true;
            }
        });
}

function fetchAttemptedQuestions() {
    fetch("/get_attempted_questions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId })
    })
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("question-list");
            list.innerHTML = ""; 

            data.attempted_questions.forEach(entry => {
                const item = document.createElement("div");
                item.className = "question-item";
                item.innerHTML = `Q${entry.question_id} - ${entry.concept}: Score ${entry.understanding_score}`;
                item.addEventListener("click", () => {
                    currentQuestionId = entry.question_id;
                    currentQuestionText = entry.question_text;
                    currentConcept = entry.concept;
                    questionOutput.textContent = entry.question_text;
                });
                list.appendChild(item);
            });
        });
}

submitButton.addEventListener("click", () => {
    const userCode = editor.getValue();

    fetch("/submit_answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            user_id: userId,
            question_id: currentQuestionId,
            question_text: currentQuestionText,
            concept: currentConcept,
            code: userCode
        })
    })
        .then(res => res.json())
        .then(data => {
            const feedbackEl = document.getElementById("submission-feedback");
            feedbackEl.innerHTML = `<p>💡 <strong>Score:</strong> ${data.score}</p><p><strong>Response:</strong> ${marked.parse(data.response)}</p>`;
            const coinDisplay = document.getElementById('coins');
            coinDisplay.innerText = `💰 Coins: ${data.coins}`;
            fetchNextQuestion();
        });
});

window.onload = () => {
    fetchNextQuestion();
    fetchAttemptedQuestions();
};
