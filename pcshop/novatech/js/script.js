console.log("Nova Tech Website Loaded");

document.querySelectorAll('.btn-custom').forEach(button => {
    button.addEventListener('mouseover', () => {
        button.style.opacity = '0.9';
    });

    button.addEventListener('mouseout', () => {
        button.style.opacity = '1';
    });
});
