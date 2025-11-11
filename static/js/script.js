'use strict';

/**
 * Point d'entrée du JavaScript côté client.
 * Ce fichier gère les interactions dynamiques de la page.
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('Page chargée et prête.');

    // Sélection des éléments
    const form = document.querySelector('form');

    // Gestion du formulaire de contact
    if (form) {
        form.addEventListener('submit', (event) => {
            event.preventDefault();

            // Récupérer les données du formulaire
            const formData = new FormData(form);
            const data = {
                name: formData.get('user_name'),
                email: formData.get('user_email'),
                message: formData.get('user_message'),
            };

            console.log('Données du formulaire:', data);

            // Réinitialiser le formulaire
            form.reset();

            // Afficher un message de succès (optionnel)
            alert('Merci ! Votre message a été envoyé.');
        });
    }

    // Fonction pour le smooth scroll des liens d'ancrage (déjà géré par CSS, mais utile en fallback)
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href !== '#') {
                const target = document.querySelector(href);
                if (target) {
                    // Le scroll smooth est géré par html { scroll-behavior: smooth; }
                    // Mais on peut ajouter une logique personnalisée si nécessaire
                }
            }
        });
    });
});
