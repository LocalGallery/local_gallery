$(function () {

    let renderLocation = function (name, info, lat, lng) {
        return `<h3>${name}</h3><div>${info}</div><br/>${lat}:${lng}`;
    };

    const formUrl = $('.locations').data('create-url');

    const map = L.map('map').setView([32, 35], 8);

    const layer = L.tileLayer('https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 16
    });

    layer.addTo(map);

    map.on('click', e => {
        let autoRemove = true;
        const latlng = e.latlng;
        const marker = L.marker(latlng);
        const loading = $("<div>loading...</div>");
        $.get(formUrl, resp => {
            const content = $(resp.trim());
            content.find("#id_lat").val(latlng.lat);
            content.find("#id_lng").val(latlng.lng);
            loading.empty().append(content);
            marker.getPopup().update();
            const form = $(content.find("form"));
            form.on('click', 'button', () => {
                const data = {
                    'name': form.find("#id_name").val(),
                    'information': form.find("#id_information").val(),
                    'lat': latlng.lat,
                    'lng': latlng.lng
                };
                loading.html("saving....");
                autoRemove = false;
                $.post(formUrl, data, (resp) => {
                    const msg = renderLocation(resp.name, resp.info, resp.lat, resp.lng);
                    marker.getPopup().setContent(msg);
                    marker.closePopup();
                });
                return false;
            });
        });

        marker.addTo(map);
        marker.bindPopup(loading.get(0)).openPopup();
        marker.on('popupclose', () => {
            if (autoRemove) {
                marker.remove();
            }
        });
    });

    const places = $('.location');
    places.each((i, el) => {
        const place = $(el);
        const lat = place.data('lat');
        const lng = place.data('lng');
        console.log(lat, lng);
        const marker = L.marker([lat, lng]);
        marker.addTo(map);

        const name = place.find('.name').html();
        const info = place.find('.info').html();
        marker.bindPopup(renderLocation(name, info, lat, lng));
    });

});
