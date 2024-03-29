$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log(id)

    $.ajax({
        type:'GET',
        url:"/pluscart",
        data:{
            movie_id :id
        },
        success: function(data){
            $(eml).text(data.quantity);
            document.getElementById("totalamount").innerText=data.totalamount
            document.getElementById("SGST").innerText=data.SGST
            document.getElementById("CGST").innerText=data.CGST
        }

    })
});


$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log(id)

    $.ajax({
        type:'GET',
        url:"/minuscart",
        data:{
            movie_id :id
        },
        success: function(data){
            $(eml).text(data.quantity);
            document.getElementById("totalamount").innerText=data.totalamount
            document.getElementById("SGST").innerText=data.SGST
            document.getElementById("CGST").innerText=data.CGST
        }

    })
});

$(document).ready(function() {
    $('.remove-cart').click(function () {
        var id = $(this).attr("pid").toString();
        var eml = this;
        console.log(id);

        $.ajax({
            type: 'GET',
            url: "/removecart",
            data: {
                movie_id: id
            },
            success: function(data) {
                // Update the elements displaying total amount, CGST, and SGST
                $('#totalamount').text(data.total_amount);
                $('#SGST').text(data.SGST);
                $('#CGST').text(data.CGST);
                
                // Optionally, you can remove the entire cart item element from the DOM
                $(eml).closest('.card').remove();
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log(xhr.statusText);
                console.log(textStatus);
                console.log(errorThrown);
            }
        });
    });
});


// $('.remove-cart').click(function () {
//     var id = $(this).attr("pid").toString();
//     var eml = this;
//     console.log(id);

//     $.ajax({
//         type: 'GET',
//         url: "/removecart",
//         data: {
//             movie_id: id
//         },
//         success: function(data) {
//             // Update the elements displaying total amount, CGST, and SGST
//             $('#totalamount').text(data.total_amount);
//             $('#SGST').text(data.SGST);
//             $('#CGST').text(data.CGST);
            
//             // Optionally, you can remove the entire cart item element from the DOM
//             $(eml).closest('.card').remove();
//         },
//         error: function(xhr, textStatus, errorThrown) {
//             console.log(xhr.statusText);
//             console.log(textStatus);
//             console.log(errorThrown);
//         }
//     });
// });


