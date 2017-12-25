$(function () {
    console.log("load");

    const map = L.map('map').setView([32, 35], 8);

    const layer = L.tileLayer('https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 16
    });

    layer.addTo(map);

    map.on('click', e => {
        const latlng = e.latlng;
        console.log(latlng);
        const marker = L.marker(latlng);
        marker.addTo(map);
        marker.bindPopup(`<b>${latlng.lat}:${latlng.lng}</b>`).openPopup();
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
        marker.bindPopup(`<b>${name}</b><br/>${lat}:${lng}`).openPopup();
    });

});
