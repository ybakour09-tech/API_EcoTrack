
async function loadUsers() {
    try {
        const users = await apiGet('/users/');
        const container = document.getElementById('users-list');

        container.innerHTML = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Email</th>
                        <th>Rôle</th>
                        <th>Statut</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${users.map(user => `
                        <tr>
                            <td>${user.id}</td>
                            <td>${user.email}</td>
                            <td>
                                <select onchange="updateUser(${user.id}, 'role', this.value)" class="form-select">
                                    <option value="user" ${user.role === 'user' ? 'selected' : ''}>Utilisateur</option>
                                    <option value="admin" ${user.role === 'admin' ? 'selected' : ''}>Administrateur</option>
                                </select>
                            </td>
                            <td>
                                <select onchange="updateUser(${user.id}, 'is_active', this.value === 'true')" class="form-select">
                                    <option value="true" ${user.is_active ? 'selected' : ''}>Actif</option>
                                    <option value="false" ${!user.is_active ? 'selected' : ''}>Inactif</option>
                                </select>
                            </td>
                            <td>
                                <button onclick="deleteUser(${user.id})" class="btn btn-danger btn-sm">Supprimer</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        console.error('Erreur:', error);
        showError('users-list', 'Erreur chargement utilisateurs');
    }
}

async function updateUser(userId, field, value) {
    try {
        const payload = {};
        payload[field] = value;

        const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Erreur mise à jour');

        // Recharger pour confirmer
        loadUsers();
    } catch (error) {
        showError('users-list', error.message);
    }
}

async function deleteUser(userId) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur ?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });

        if (!response.ok) throw new Error('Erreur suppression');

        loadUsers();
    } catch (error) {
        showError('users-list', error.message);
    }
}
