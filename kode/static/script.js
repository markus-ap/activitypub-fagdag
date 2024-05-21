window.onload = function() {
    var form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        var input = document.querySelector('input[name="resource"]');
        input.value = input.value.trim();
        if (input.value.indexOf('@') === 0) {
            input.value = 'acct:' + input.value;
        }
        form.submit();
    });
};