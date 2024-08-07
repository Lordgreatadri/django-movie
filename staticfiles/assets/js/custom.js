
jQuery(function(e) {
    toastr.options.closeButton = true;
    toastr.options.timeOut = 10000;
    toastr.options.extendedTimeOut = 45;
    toastr.options.hideMethod = 'slideUp';
    toastr.options.closeEasing = 'linear';
    toastr.options.showMethod = 'slideDown';
    toastr.options.closeMethod = 'slideUp';
});


function showModal(element) {
    // Retrieve data attributes
    const title = element.getAttribute('data-title');
    const description = element.getAttribute('data-description');
    const releaseDate = element.getAttribute('data-release-date');
    const genre = element.getAttribute('data-genre');
    const length = element.getAttribute('data-length');
    const imageCardUrl = element.getAttribute('data-image-card-url');
    const imageCoverUrl = element.getAttribute('data-image-cover-url');
    const dataVideoUrl = element.getAttribute('data-video-url');

    // Update the modal's content with the movie details
    const modal = document.getElementById('movieModal');
    modal.querySelector('.modal-content h2').textContent = title;
    modal.querySelector('.modal-content img').src = imageCoverUrl;
    modal.querySelector('.modal-content a').href = dataVideoUrl;  
    modal.querySelector('.modal-content img').alt = title + " Cover Image";
    modal.querySelector('.modal-content .flex span:first-child').textContent = "Year: " + releaseDate;
    modal.querySelector('.modal-content .flex span:nth-child(2)').textContent = "Genre: " + genre;
    modal.querySelector('.modal-content .flex span:last-child').textContent = "Length: " + length + "min";
    modal.querySelector('.modal-content p').textContent = description;

    // Show the modal
    modal.style.display = 'block';
    setTimeout(() => {
        modal.classList.add('modal-show');
    }, 50);
}

function hideModal() {
    const modal = document.querySelector('.modal');
    modal.classList.remove('modal-show');
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
}


window.onclick = function(event) {
    if (event.target === document.getElementById('movieModal')) {
        hideModal();
    }
}


function addItemToList() {

    const modal = document.getElementById('movieModal')
    var movieID = modal.querySelector('.modal-content a').href;
    const search = document.getElementById('search');
    var csrf_token = search.querySelector('input[type=hidden]');
    // var csrf_token = window.getElementById('csrfmiddlewaretoken');
    $.ajax({
        // url: "{% url 'add-to-list' %}",
        url: "/add-to-list",
        type: "POST",
        data: {
            movie_uuid: movieID,
            // csrfmiddlewaretoken: "{{ csrf_token }}"
            csrfmiddlewaretoken: csrf_token.value
        },
        success: function(data) {
            if(data.code == 200) {
                $('#addToListbtn').text("Movie Added");

                $('#addToListbtn').prop('disabled', true);
                toastr.success('Movie Added Successfully!', 'Success!');

                console.log("Item added to list!");
            }else {
                toastr.error(data.message, 'Alert!');
                console.error("Error adding item to list: " + data.message);
            }
        },
        error: function(xhr, errmsg, err) {
            toastr.warning(errmsg, 'Warning!');
            console.error("Something went wrong adding item to list: " + errmsg);
        }
    });
}