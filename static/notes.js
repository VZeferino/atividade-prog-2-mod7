document.getElementById('addNoteForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const note = document.getElementById('newNote').value;

    const response = await fetch(`/notes/teste`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ note })
    });

    if (response.ok) {
        // Depois de adicionar a nota, carregar novamente todas as notas
        loadNotes();
        document.getElementById('newNote').value = ''; // Limpar o campo de texto
    } else {
        alert('Erro ao adicionar nota');
    }
});

async function loadNotes() {
    const response = await fetch(`/notes/teste`);
    const data = await response.json();

    // Limpar a lista antes de adicionar as novas notas
    const notesList = document.getElementById('notesList');
    notesList.innerHTML = '';

    data.notes.forEach((note, index) => {
        const li = document.createElement('li');
    
        // Adiciona o texto da nota ao <li>
        li.appendChild(document.createTextNode(note.note));
    
        // Adiciona o emoji de edição ao <li>
        const editEmoji = document.createElement('span');
        editEmoji.textContent = '✏️';
        editEmoji.className = 'edit-emoji';
        editEmoji.setAttribute('data-id', note.id);
        li.appendChild(editEmoji);
    
        // Adiciona o emoji de exclusão ao <li>
        const deleteEmoji = document.createElement('span');
        deleteEmoji.textContent = '🗑️';
        deleteEmoji.className = 'delete-emoji';
        deleteEmoji.setAttribute('data-id', note.id);
        li.appendChild(deleteEmoji);
    
        notesList.appendChild(li);

    });
    
    // Adicionar evento de clique a emojis de edição
    document.querySelectorAll('.edit-emoji').forEach(editEmoji => {
        editEmoji.addEventListener('click', function() {
            const noteId = editEmoji.getAttribute('data-id');
            const noteIndex = data.notes.findIndex(note => note.id === parseInt(noteId));
            const noteText = data.notes[noteIndex].note; // Obter o texto da nota corretamente
    
            const updatedNote = prompt("Editar nota:", noteText);
    
            if (updatedNote !== null) {
                updateNote(noteId, updatedNote);
            }
        });
    });
    
    // Adicionar evento de clique a emojis de exclusão
    document.querySelectorAll('.delete-emoji').forEach(deleteEmoji => {
        deleteEmoji.addEventListener('click', function() {
            const noteId = deleteEmoji.getAttribute('data-id');
            if (confirm("Tem certeza de que deseja excluir esta nota?")) {
                deleteNote(noteId);
            }
        });
    });
}

async function updateNote(noteId, updatedText) {
    const response = await fetch(`/notes/teste/${noteId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ note: updatedText })
    });

    if (response.ok) {
        // Recarregar as notas após a atualização
        loadNotes();
    } else {
        alert('Erro ao atualizar nota');
    }
}

async function deleteNote(noteId) {
    const response = await fetch(`/notes/teste/${noteId}`, {
        method: 'DELETE',
    });

    if (response.ok) {
        // Recarregar as notas após a exclusão
        loadNotes();
    } else {
        alert('Erro ao excluir nota');
    }
}

// Carregar notas ao carregar a página
loadNotes();

// Adicionar evento de clique a um elemento pai (delegado)
document.getElementById('notesList').addEventListener('click', function(event) {
    const target = event.target;
    if (target.classList.contains('edit-button')) {
        const noteIndex = parseInt(target.getAttribute('data-index'));
        const noteText = data.notes[noteIndex].note; // Supondo que data.notes seja acessível aqui
        const updatedNote = prompt("Editar nota:", noteText);

        if (updatedNote !== null) {
            updateNote(noteIndex, updatedNote);
        }
    }
});
