document.addEventListener('DOMContentLoaded', function() {
    // Handle suggested dish clicks
    const suggestedDishes = document.querySelectorAll('.suggested-dish');
    const dishInput = document.getElementById('dish_name');
    
    if (suggestedDishes && dishInput) {
        suggestedDishes.forEach(dish => {
            dish.addEventListener('click', function() {
                const dishName = this.getAttribute('data-dish');
                dishInput.value = dishName;
                
                // Scroll to the form
                document.querySelector('form').scrollIntoView({ behavior: 'smooth' });
                
                // Focus on the input
                dishInput.focus();
            });
        });
    }
    
    // Automatically dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    if (alerts) {
        alerts.forEach(alert => {
            setTimeout(() => {
                const closeButton = alert.querySelector('.btn-close');
                if (closeButton) {
                    closeButton.click();
                }
            }, 5000);
        });
    }
});
