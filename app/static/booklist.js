$(function () {
    var editbtn = $("button.edit");
    var deletetbtn = $("button.delete");


    deletetbtn.click(function () {
        var bookid = $(this).parents('li').attr('data-id');
        $.myConfirm({
            message: "确定要删除吗",
            title: '温馨提示',
            callback: function () {
                deletebook(bookid)
            }
        })

        function deletebook(bookid) {
            $.ajax({
                url: "/delete_book/" + "?book_id=" + bookid,
                type: "GET",
                dataType: "json",

            }).done(function (ret) {
                if (ret["code"] === 200) {
                    window.location.reload()
                }
            })
        }
    })


})

