// Fichier JavaScript principal pour l'application VoiceStudio

// Fonction pour afficher les notifications
function showNotification(message, type = 'info') {
    // Créer l'élément de notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close">×</button>
    `;
    
    // Ajouter au conteneur de notifications (créer si nécessaire)
    let container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        document.body.appendChild(container);
    }
    
    container.appendChild(notification);
    
    // Gérer la fermeture
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        notification.classList.add('notification-hide');
        setTimeout(() => {
            notification.remove();
        }, 300);
    });
    
    // Auto-fermeture après 5 secondes
    setTimeout(() => {
        if (notification.parentNode) {
            notification.classList.add('notification-hide');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }, 5000);
}

// Fonction pour afficher un overlay de chargement
function showLoading(message = 'Chargement en cours...') {
    // Créer l'overlay s'il n'existe pas
    let overlay = document.getElementById('loading-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="spinner-border loading-spinner text-light" role="status">
                <span class="visually-hidden">Chargement...</span>
            </div>
            <div class="loading-text">${message}</div>
        `;
        document.body.appendChild(overlay);
    } else {
        overlay.querySelector('.loading-text').textContent = message;
        overlay.style.display = 'flex';
    }
}

// Fonction pour masquer l'overlay de chargement
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

// Fonction pour formater la taille des fichiers
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' octets';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(2) + ' Ko';
    else if (bytes < 1073741824) return (bytes / 1048576).toFixed(2) + ' Mo';
    else return (bytes / 1073741824).toFixed(2) + ' Go';
}

// Fonction pour effectuer des requêtes AJAX
function ajaxRequest(url, method = 'GET', data = null, isFormData = false) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open(method, url, true);
        
        if (!isFormData) {
            xhr.setRequestHeader('Content-Type', 'application/json');
        }
        
        xhr.onload = function() {
            if (this.status >= 200 && this.status < 300) {
                try {
                    const response = JSON.parse(xhr.responseText);
                    resolve(response);
                } catch (e) {
                    resolve(xhr.responseText);
                }
            } else {
                reject({
                    status: this.status,
                    statusText: xhr.statusText,
                    response: xhr.responseText
                });
            }
        };
        
        xhr.onerror = function() {
            reject({
                status: this.status,
                statusText: xhr.statusText
            });
        };
        
        if (data) {
            if (isFormData) {
                xhr.send(data);
            } else {
                xhr.send(JSON.stringify(data));
            }
        } else {
            xhr.send();
        }
    });
}

// Fonction pour rafraîchir la liste des modèles
function refreshModelsList() {
    return ajaxRequest('/api/download/models')
        .then(response => {
            return response.models;
        })
        .catch(error => {
            showNotification('Erreur lors de la récupération des modèles: ' + error.statusText, 'error');
            return [];
        });
}

// Fonction pour générer une forme d'onde aléatoire
function generateRandomWaveform(container) {
    container.innerHTML = '';
    for (let i = 0; i < 100; i++) {
        const height = Math.floor(Math.random() * 80) + 10;
        const bar = document.createElement('div');
        bar.className = 'waveform-bar';
        bar.style.height = height + 'px';
        container.appendChild(bar);
    }
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Créer le conteneur de notifications s'il n'existe pas
    if (!document.getElementById('notification-container')) {
        const container = document.createElement('div');
        container.id = 'notification-container';
        document.body.appendChild(container);
    }
    
    // Créer l'overlay de chargement s'il n'existe pas
    if (!document.getElementById('loading-overlay')) {
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'loading-overlay';
        overlay.style.display = 'none';
        overlay.innerHTML = `
            <div class="spinner-border loading-spinner text-light" role="status">
                <span class="visually-hidden">Chargement...</span>
            </div>
            <div class="loading-text">Chargement en cours...</div>
        `;
        document.body.appendChild(overlay);
    }
});
