var homepage = (function()
{
	var songField, infoDiv, songsList, audio, currentlyPlaying, removeButton;

	function keyPressed()
	{
		var val = songField.value;
		val = val.replace(" ", "+");

		if(val.length > 0)
		{
			$.ajax({
				url:"https://api.spotify.com/v1/search?q=" + val + "&type=track",

				error: function(jqXHR, textStatus, errorThrown) {
					alert(textStatus + ': ' + errorThrown);
				},
				success: successFunction,
				type:'GET',
			});
		}

		else{
			infoDiv.innerHTML = 'Result will be displayed here';
			infoDiv.setAttribute('url', '');
			infoDiv.setAttribute('title', '');
		}
	}

	function successFunction(data)
	{
		try{
			var title = data.tracks.items[0].name;
			var url = data.tracks.items[0].preview_url;
			infoDiv.innerHTML = title;
			infoDiv.setAttribute('url', url);
			infoDiv.setAttribute('title', title);
		}
		catch(err){
			console.log('Sorry, no song to display');
		}
	}

	function changeSong(target)
	{
		event.preventDefault();

		for(var i = 0; i < songsList.length; i++)
		{
			if(songsList[i] == target)
				songsList[i].setAttribute('class', 'collection-item active');

			else
				songsList[i].setAttribute('class', 'collection-item');
		}

		currentlyPlaying.innerHTML = target.innerText.split("Remove")[0];
		audio.src = target.getAttribute('url');
		audio.play();
	}

	function addNewSong()
	{
		var title = infoDiv.getAttribute('title');
		var url = infoDiv.getAttribute('url');

		if(title.length == 0 || url.length == 0)
			return;

		for(var i = 0; i < songsList.length; i++)
		{
			if(url == songsList[i].getAttribute('url'))
			{
				changeSong(songsList[i]);
				songField.value = '';
				songField.blur();
				infoDiv.innerHTML = 'Result will be displayed here';
				infoDiv.setAttribute('url', '');
				infoDiv.setAttribute('title', '');
				return;				
			}
		}

		$.ajax({
			url : "/playlist/add-song/",
			type : 'POST',
			data : {'title' : title, 'url' : url},
			success : function(data){console.log(data); window.location.href = '/'},
			error : function(jqXHR, textStatus, errorThrown) {
				alert(textStatus + ': ' + errorThrown);
			},
		});

		var newSong = document.createElement('a');
		newSong.setAttribute('url', url);
		newSong.setAttribute('title', title);



		changeSong(newSong);
	}

	function deleteSong(target, e)
	{
		console.log(e);
		e.stopPropagation();
		$.ajax({
			url : '/playlist/remove-song/',
			type : 'POST',
			data : {'title' : target.getAttribute('title'), 'url' : target.getAttribute('url')},
			success : function(data){ console.log(data); },
		});
		target.parentNode.style.display = 'none';
	}

	function init(obj)
	{
		songField = document.getElementById(obj.songField);
		infoDiv = document.getElementById(obj.infoDiv);
		songsList = document.querySelectorAll(obj.songsList);
		audio = document.getElementById(obj.audio);
		currentlyPlaying = document.getElementById(obj.currentlyPlaying);
		removeButton = document.getElementsByClassName(obj.removeButton);

		infoDiv.addEventListener('click', addNewSong);
		songField.addEventListener('keyup', keyPressed);

		for(var i = 0; i < songsList.length; i++)
			songsList[i].addEventListener('click', changeSong.bind(this, songsList[i]));

		for(var i = 0; i < removeButton.length; i++)
			removeButton[i].addEventListener('click', deleteSong.bind(this, removeButton[i]));
	}

	return {
		'init' : init,
	};
})();













