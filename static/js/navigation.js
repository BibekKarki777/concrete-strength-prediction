document.querySelectorAll('[data-menu-toggle]').forEach((button) => {
    const panel = document.getElementById(button.getAttribute('aria-controls'));
    const close = () => {
        panel.classList.remove('is-open');
        button.setAttribute('aria-expanded', 'false');
    };
    button.addEventListener('click', () => {
        const open = button.getAttribute('aria-expanded') !== 'true';
        panel.classList.toggle('is-open', open);
        button.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {
            close();
            button.focus();
        }
    });
    document.addEventListener('click', (event) => {
        if (!panel.contains(event.target) && !button.contains(event.target)) close();
    });
    window.matchMedia('(min-width: 992px)').addEventListener('change', close);
});


const deleteDialog = document.getElementById('delete-confirmation');
let pendingDeleteForm = null;
let deleteTrigger = null;

if (deleteDialog) {
    const confirmButton = deleteDialog.querySelector('[data-delete-confirm]');
    const cancelButton = deleteDialog.querySelector('[data-delete-cancel]');

    document.querySelectorAll('[data-confirm-delete]').forEach((form) => {
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            pendingDeleteForm = form;
            deleteTrigger = event.submitter || document.activeElement;
            confirmButton.disabled = false;
            deleteDialog.showModal();
            cancelButton.focus();
        });
    });

    cancelButton.addEventListener('click', () => {
        deleteDialog.close();
    });

    deleteDialog.addEventListener('close', () => {
        pendingDeleteForm = null;
        if (deleteTrigger && deleteTrigger.isConnected) {
            deleteTrigger.focus();
        }
        deleteTrigger = null;
    });

    confirmButton.addEventListener('click', () => {
        if (!pendingDeleteForm || confirmButton.disabled) {
            return;
        }
        confirmButton.disabled = true;
        // Submit only the selected row's existing POST form, including its CSRF token.
        HTMLFormElement.prototype.submit.call(pendingDeleteForm);
    });
}
