
var map;
var markers = [];
var infoWindow;
var locationSelect;

function initMap() {
    var losAngeles = {
        lat: 51.5221042,
        lng: -0.3817765
    };
    map = new google.maps.Map(document.getElementById('map'), {
        center: losAngeles,
        zoom: 11,
        mapTypeId: 'roadmap',
    });
    infoWindow = new google.maps.InfoWindow();
    searchStores();
}

let searchInput = document.getElementById('search-input');

window.addEventListener('load', function(event){
    if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                // Get the user's latitude and longitude
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                // Store the location in a cookie
                document.cookie = `latitude=${latitude}; path=/`;
                document.cookie = `longitude=${longitude}; path=/`;
                console.log(document.cookie)
                // Optionally, you can redirect or display a message here
            });
        } else {
            console.warn('Geolocation is not supported in this browser.');
        }
});

searchInput.addEventListener('keyup', function(event){
    if (event.key === "Enter") {
        searchStores().then(r => console.log("searched"));
    }
});
async function searchStores() {
    var searchTerm = document.getElementById('search-input').value;
    var url = '/api/v1/tasks/';

    try {
        var response = await  fetch(url, {method: 'GET'});
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        var data = await response.json();
        console.log("data has been fetched successfully")
        console.log(data);
        var foundStores = filterStores(data, searchTerm);
        console.log(foundStores);
        clearLocations();
        console.log("clear locations")
        displayStores(foundStores);
        console.log("display tasks")
        showStoreMarkers(foundStores);
        console.log("show store markers")
        setOnClickListener();
        console.log("set on click listener")
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function filterStores(tasks, searchTerm) {
    if (searchTerm) {
        return tasks.filter(function(task){
            return task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                task.location.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                task.description.toLowerCase().includes(searchTerm.toLowerCase());
        })
    } else {
        return tasks;
    }
}



function clearLocations() {
    infoWindow.close();
    for (var i = 0; i < markers.length; i++) {
      markers[i].setMap(null);
    }
    markers.length = 0;
  }

function setOnClickListener(){
    var storeElements = document.querySelectorAll('.store-container');
    storeElements.forEach(function(elem, index){
        elem.addEventListener('click', function(){
            new google.maps.event.trigger(markers[index], 'click');
        })
    })
}

function displayStores(tasks){
    var tasksHtml = '';
    tasks.forEach(function(task, index){
        var locationName = task.location.name;
        var name = task.title;
        console.log(task)
        tasksHtml += `
            <div class="store-container">
                <div class="store-container-background">
                    <div class="store-info-container">
                        <div class="store-address">
                            <span>${name}</span>
                        </div>
                        <div class="store-phone-number text-capitalize">Estimated distance is ${task.estimated_distance}</div>
                        <div class="store-phone-number text-capitalize">Estimated time is ${task.estimated_time}</div>
                        <div class="store-phone-number text-capitalize">Suggested Route Distance: ${task.route_suggestion.distance} 
                        Time: ${task.route_suggestion.duration} Steps: ${task.route_suggestion.steps}</div>
                    </div>
                    <div class="store-number-container">
                        <div class="store-number">${task.location.tasks}</div>
                    </div>
                </div>
            </div>
        `
    });

    document.querySelector('.stores-list').innerHTML = tasksHtml;
}



function showStoreMarkers(tasks){
    var bounds = new google.maps.LatLngBounds();
    tasks.forEach(function(task, index){
        console.log(task.location.coordinates.coordinates)
        var latlng = new google.maps.LatLng(
            task.location.coordinates.coordinates[1],
            task.location.coordinates.coordinates[0]);

        var name = task.title;
        var estimatedDistance = `Estimated distance is ${task.estimated_distance}`;
        var estimatedTime = `Estimated time is ${task.estimated_time}`;
        var suggestedRouteDistance = `Suggested Route Distance: ${task.route_suggestion.distance} 
        Time: ${task.route_suggestion.duration} Steps: ${task.route_suggestion.steps}`;
        console.log(estimatedDistance)
        createMarker(latlng, name, estimatedDistance, task.location.tasks, estimatedTime, suggestedRouteDistance);
        bounds.extend(latlng);
    })
    map.fitBounds(bounds);
}


function createMarker(latlng, name, estimatedDistance, tasksCount, estimatedTime, suggestedRouteDistance){
    var html = "<b>" + name + "</b> <br/>" + estimatedDistance+ "</b> <br/>" + estimatedTime+ "</b> <br/>" + suggestedRouteDistance;
    var marker = new google.maps.Marker({
      map: map,
      position: latlng,
      label: `${tasksCount}`
    });
    google.maps.event.addListener(marker, 'click', function() {
      infoWindow.setContent(html);
      infoWindow.open(map, marker);
    });
    markers.push(marker);
}