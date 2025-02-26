'use strict';

const modal = document.querySelector('.modal');
const btnCloseModal = document.querySelector('.close-modal');

const closeModal = function() {
    modal.classList.add('hidden');
}

btnCloseModal.addEventListener('click', closeModal);

