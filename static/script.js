document.addEventListener('DOMContentLoaded', function() {
    const userInputElement = document.getElementById('user-input');
    const chatbotElement = document.getElementById('chatbot');
    const sendButtonElement = document.getElementById('send-button');

//    function formatMessage(text) {
//        // Échapper les caractères HTML spéciaux
//        text = text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
//
//        // Gérer les blocs de code ``` (multi-lignes)
//        text = text.replace(/```(\w+)?([\s\S]*?)```/g, (match, lang, code) => {
//            return `<pre><code class="language-${lang || 'javascript'}">${code}</code></pre>`;
//        });
//
//        // Gérer les codes inline `code`
//        text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
//
//        text = text.replace(/^##\s(.*)$/gm, '<h2>$1</h2>');
//        text = text.replace(/^#\s(.*)$/gm, '<h1>$1</h1>');
//
//
//        text = text.replace(/^\s*[-*]\s+(.*)$/gm, '<ul><li>$1</li></ul>');
//
//        text = text.replace(/<\/ul>\s*<ul>/g, '');
//
//        text = text.replace(/^\s*\d+\.\s+(.*)$/gm, '<ol><li>$1</li></ol>');
//
//        text = text.replace(/<\/ol>\s*<ol>/g, '');
//
//        text = text.replace(/\n\n+/g, '</p><p>');
//        text = '<p>' + text + '</p>';
//
//        return text;
//    }

    function typeWriterEffect(element, text, index = 0, speed = 10) {
        if (index === 0) {
//            text = formatMessage(text); // On applique le formatage une seule fois avant de commencer l'effet
            element.innerHTML = ''; // Vide l'élément avant d'écrire
            element.dataset.fullText = text; // Stocke le texte formaté
        }

        if (index < element.dataset.fullText.length) {
            // Ajoute le texte sous forme de HTML sans écrire les balises en tant que texte brut
            element.innerHTML = element.dataset.fullText.slice(0, index + 1);
            setTimeout(() => typeWriterEffect(element, text, index + 1, speed), speed);
            chatbotElement.scrollTop = chatbotElement.scrollHeight;
        }
    }

    function sendMessage(userInput) {
        const userMessageElement = document.createElement('div');
        userMessageElement.classList.add('user');
        userMessageElement.textContent = userInput;
        chatbotElement.appendChild(userMessageElement);
        chatbotElement.scrollTop = chatbotElement.scrollHeight;

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/ask', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                const botMessageElement = document.createElement('div');
                botMessageElement.classList.add('bot');
                chatbotElement.appendChild(botMessageElement);

                typeWriterEffect(botMessageElement, response.response);


            }
        };
        xhr.send('user_message=' + encodeURIComponent(userInput));
    }

    userInputElement.addEventListener('keyup', function(event) {
        if (event.keyCode === 13) {
            const userInput = userInputElement.value;
            userInputElement.value = '';
            sendMessage(userInput);
        }
    });

    sendButtonElement.addEventListener('click', function() {
        const userInput = userInputElement.value;
        userInputElement.value = '';
        sendMessage(userInput);
    });

    document.getElementById('buttonDet').addEventListener('click', function() {
        fetch('/detection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    document.getElementById('buttonDisco').addEventListener('click', function() {
        fetch('/segmentation_disco', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    document.getElementById('buttonSeg').addEventListener('click', function() {
        fetch('/segmentation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });


});


window.addEventListener("load", function() {
    let detection = document.querySelector(".detection");
    let chatbot = document.querySelector(".chatbot");

    let maxHeight = Math.max(chatbot.clientHeight, detection.clientHeight);
    chatbot.style.height = detection.style.height = maxHeight + "px";
});

function onSelectChange() {
    // Récupérer la valeur sélectionnée
    const choix = document.getElementById("choix").value;

    // Créer une requête AJAX pour envoyer les données au serveur
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/submit", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    // Gestion de la réponse du serveur
    xhr.onload = function() {
        if (xhr.status === 200) {
            document.getElementById("result").innerHTML = xhr.responseText;
        }
    };

    // Envoyer la requête avec la valeur sélectionnée
    xhr.send("choix=" + encodeURIComponent(choix));
}