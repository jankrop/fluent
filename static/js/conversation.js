document.addEventListener('DOMContentLoaded', function() {
    const recordingIndicator = document.getElementById('recIndicator');

    let mediaRecorder;

    document.addEventListener('keypress', async ev => {
        if (ev.key !== ' ') return

        try {
            let audioChunks = [];

            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                console.log('NEW CHUNK!')
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                sendAudioToServer(audioBlob);
            };

            recordingIndicator.style.display = 'inline';

            mediaRecorder.start();
        } catch (error) {
            console.error('Error accessing microphone:', error);
        }
    })

    document.addEventListener('keypress', ev => {
        if (ev.key !== 'a') return;

        recordingIndicator.style.display = 'none';
        mediaRecorder.stop();
    });

    function sendAudioToServer(audioBlob) {
        const formData = new FormData();

        formData.append('audio', audioBlob, 'recording.wav');

        fetch(messageURL, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            const audioCtx = new AudioContext();
            const buffer = audioCtx.createBuffer(1, data.audio.length, data.sr);
            const channelData = buffer.getChannelData(0);

            for (let i = 0; i < data.audio.length; i++) {
                channelData[i] = data.audio[i]
            }

            const source = audioCtx.createBufferSource();
            source.buffer = buffer;
            source.connect(audioCtx.destination);
            source.start();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});