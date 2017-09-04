// 当文档完成加载时，我们为"Add to Cart"按钮添加了点击事件处理函数，并隐藏了"Remove form Cart"按钮。
// 这些事件处理函数关联服务器的API调用，并交换添加到购物车接口和从购物车移除接口。
$(document).ready(function() {
    document.session = $('#session').val();

    setTimeout(requestInventory, 100);

    $('#add-button').click(function(event) {
        jQuery.ajax({
            url: '//localhost:8000/cart',
            type: 'POST',
            data: {
                session: document.session,
                action: 'add'
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                $(event.target).attr('disabled', 'disabled');
            },
            success: function(data, status, xhr) {
                $('#add-to-cart').hide();
                $('#remove-from-cart').show();
                $(event.target).removeAttr('disabled');
            }
        });
    });

    $('#remove-button').click(function(event) {
        jQuery.ajax({
            url: '//localhost:8000/cart',
            type: 'POST',
            data: {
                session: document.session,
                action: 'remove'
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                $(event.target).attr('disabled', 'disabled');
            },
            success: function(data, status, xhr) {
                $('#remove-from-cart').hide();
                $('#add-to-cart').show();
                $(event.target).removeAttr('disabled');
            }
        });
    });
});

// requestInventory函数在页面完成加载后经过一个短暂的延迟再进行调用。
function requestInventory() {
    // 通过到/cart/status的HTTP GET请求初始化一个长轮询
    jQuery.getJSON('//localhost:8000/cart/status', {session: document.session},
        function(data, status, xhr) {
            $('#count').html(data['inventoryCount']);
            setTimeout(requestInventory, 0);
        }
    );
}