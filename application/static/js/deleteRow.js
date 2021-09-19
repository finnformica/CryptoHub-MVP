// $('button.btnDelete').on('click', function (e) {
//     e.preventDefault();
//     var id = $(this).closest('tr').data('id');
//     $('#deleteModal').data('id', id).modal('show');
// });

$('#btnDeleteYes').click(function () {
    var id = $('#deleteModal').data('id');
    $('[data-id=' + id + ']').remove();
    $('#deleteModal').modal('hide');
});
