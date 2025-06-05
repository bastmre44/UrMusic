// Este script no esta siendo utilizado por el momento,
// pero se deja aquí por si se decide utilizarlo en un futuro.

$(document).ready(function () {
    $('.card-info').each(function () {
        let artist_name = $(this).attr('id');
        let url = 'http://localhost:5000/search';
        let card = $(this).prev('.card');
        let artist_name_header = $(this).find('h2');
        let genre_paragraph = $(this).find('p:contains("Género:")');
        let top_tracks_list = $(this).find('p:contains("Canciones destacadas:")').nextAll('p');
        $.getJSON(url, {term: artist_name}, function (data) {
            if (data.image_url) {
                card.css('background-image', 'url(' + data.image_url + ')');
            } else {
                alert(data.message);
            }
            if (data.genre) {
                let genre = data.genre.toUpperCase();
                genre_paragraph.html('<b>Género:</b> ' + genre);
            }
            if (data.top_tracks && data.top_tracks_urls) {
                top_tracks_list.each(function (index) {
                    if (index < data.top_tracks.length) {
                        $(this).html('<a href="' + data.top_tracks_urls[index] + '" target="_blank">○ ' + data.top_tracks[index] + ' <img src="static/Icons/spotify-icon.svg" style="height: 16px;" alt="Spotify icon link"></a>');
                    }
                });
            }
            let display_name = artist_name.split(/(?=[A-Z])/).join(" ");
            artist_name_header.text(display_name);
        });
    });
});
