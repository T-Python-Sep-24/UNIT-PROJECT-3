document.addEventListener('DOMContentLoaded', function() {
    // Flip card functionality
    document.querySelectorAll('.flip-btn').forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.carousel-item').querySelector('.flashcard');
            card.classList.toggle('flipped');
            this.textContent = card.classList.contains('flipped') ? 'Show Question' : 'Flip Card';
        });
    });

    // Hint functionality
    document.querySelectorAll('.hint-btn').forEach(button => {
        button.addEventListener('click', toggleContent);
    });

    // Explanation functionality
    document.querySelectorAll('.explain-btn').forEach(button => {
        button.addEventListener('click', toggleContent);
    });

    // Content toggle function
    function toggleContent(event) {
        const button = event.currentTarget;
        const isHintBtn = button.classList.contains('hint-btn');
        const contentClass = isHintBtn ? '.hint-content' : '.explain-content';
        const content = button.closest('.carousel-item').querySelector(contentClass);
        
        if (!content) return;  // Safety check
        
        // Toggle display
        if (content.style.display === 'block') {
            content.style.display = 'none';
            button.textContent = isHintBtn ? 'Show Hint' : 'Show Explanation';
        } else {
            content.style.display = 'block';
            button.textContent = isHintBtn ? 'Hide Hint' : 'Hide Explanation';
        }
    }

    // Reset card state when changing slides
    const carousel = document.getElementById('flashcardCarousel');
    if (carousel) {
        carousel.addEventListener('slide.bs.carousel', function () {
            // Reset flip state
            document.querySelectorAll('.flashcard').forEach(card => {
                card.classList.remove('flipped');
            });
            
            // Reset visibility
            document.querySelectorAll('.hint-content, .explain-content').forEach(element => {
                element.style.display = 'none';
            });
            
            // Reset buttons
            document.querySelectorAll('.flip-btn').forEach(btn => {
                btn.textContent = 'Flip Card';
            });
            document.querySelectorAll('.hint-btn').forEach(btn => {
                btn.textContent = 'Show Hint';
            });
            document.querySelectorAll('.explain-btn').forEach(btn => {
                btn.textContent = 'Show Explanation';
            });
        });
    }

    // Initialize all content to be hidden
    document.querySelectorAll('.hint-content, .explain-content').forEach(element => {
        element.style.display = 'none';
    });
});
