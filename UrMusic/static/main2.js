$(document).ready(function () {
    var artist_name = new URL(window.location.href).searchParams.get('artist');
    var baseUrl = window.location.protocol + '//' + window.location.host;
    $.ajax({
        url: baseUrl + '/api/recommend',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({artist: artist_name}),
        success: function (data) {
            console.log(data);
            if (data.length > 0) {  // Verificar si hay recomendaciones
                $('#feedback').show();
                $('#satisfaction-feedback').show();
                var recommendationsDiv = $('.card-container');
                recommendationsDiv.empty();

                data.forEach(function (artistName) {
                    var artistNameNoSpaces = artistName.replace(" ", "");

                    $.ajax({
                        url: baseUrl + '/search',
                        method: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({term: artistNameNoSpaces}),
                        success: function (data) {
                            var imageUrl = data.image_url;
                            var genre = data.genre.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');

                            var cardGroup = $('<div>').addClass('card-group');

                            var card = $('<div>').addClass('card');
                            card.css('background-image', 'url(' + imageUrl + ')');

                            var cardInfo = $('<div>').addClass('card-info');
                            var h2 = $('<h2>').text(artistName);
                            var genreElement = $('<p>').html('<b>Género:</b> ' + genre);
                            cardInfo.append(h2, genreElement);

                            cardGroup.append(card, cardInfo);

                            recommendationsDiv.append(cardGroup);

                            if (data.top_tracks && data.top_tracks_urls) {
                                var top_tracks_list = $('<ul>');
                                data.top_tracks.forEach(function (track, index) {
                                    var trackElement = $('<li>').html('<a href="' + data.top_tracks_urls[index] + '" target="_blank">' + track + ' <img src="/static/Icons/spotify-icon.svg" style="height: 16px;" alt="Spotify icon link"></a>');
                                    top_tracks_list.append(trackElement);
                                });
                                cardInfo.append('<p><b>Canciones destacadas:</b></p>', top_tracks_list);
                            }
                        }
                    });
                });
            } else {
                // Si no hay recomendaciones, mostrar mensaje
                $('body').css('margin-top', '1%');
                $('#no-recommendations').show();
            }
        }
    });

    let likeCounter = 0;
    let dislikeCounter = 0;

    $('#like-button').click(function () {
        var increment = true;
        if ($(this).hasClass('clicked')) {

            $(this).removeClass('clicked clicked-like').addClass('unclicked');
            likeCounter--;
            increment = false;
            $('#dislike-button').prop('disabled', false);
        } else {

            $(this).addClass('clicked clicked-like').removeClass('unclicked');
            likeCounter++;
            $('#dislike-button').prop('disabled', true);
        }

        // Actualizar el contador en el servidor
        $.ajax({
            url: '/api/counter',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({like: increment}),
            success: function (data) {
                $('#like-counter').text(data.likeCounter);
                $('#dislike-counter').text(data.dislikeCounter);

                fetch('/api/counter')
                    .then(response => response.json())
                    .then(data => {
                        $('#satisfaction-percentage').text("Porcentaje de satisfacción: " + data.satisfactionPercentage.toFixed(2) + "%");
                    });
            }
        });
    });

    $('#dislike-button').click(function () {
        let increment = true;
        if ($(this).hasClass('clicked')) {

            $(this).removeClass('clicked clicked-dislike').addClass('unclicked');
            dislikeCounter--;
            increment = false;
            $('#like-button').prop('disabled', false);
        } else {

            $(this).addClass('clicked clicked-dislike').removeClass('unclicked');
            dislikeCounter++;
            $('#like-button').prop('disabled', true);
        }

        // Actualizar el contador en el servidor
        $.ajax({
            url: '/api/counter',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({dislike: increment}),
            success: function (data) {
                $('#like-counter').text(data.likeCounter);
                $('#dislike-counter').text(data.dislikeCounter);

                fetch('/api/counter')
                    .then(response => response.json())
                    .then(data => {
                        $('#satisfaction-percentage').text("Porcentaje de satisfacción: " + data.satisfactionPercentage.toFixed(2) + "%");
                    });
            }
        });
    });

    fetch('/api/counter')
        .then(response => response.json())
        .then(data => {
            $('#like-counter').text(data.likeCounter);
            $('#dislike-counter').text(data.dislikeCounter);
            $('#satisfaction-percentage').text("Porcentaje de satisfacción: " + data.satisfactionPercentage.toFixed(2) + "%");
        });

});