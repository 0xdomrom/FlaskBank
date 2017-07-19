function load_account(account_num, button) {
    $.ajax({
            url: '/api/account?acc_num='+account_num,
            type: 'GET',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
}

