var paging_meta_data = {
	actual:0,
	max:0
}


function paging_init(element, link) {
	// prepare: bring to default
	$('.titlePrevIcon').removeAttr("style");
	$('.titlePrevIcon').off("click");
	$('.titleNextIcon').removeAttr("style");
	$('.titleNextIcon').off("click");

	// 1. najst tag ktory drzi data o pagingu: actual a max
	paging_meta_data.actual = $(element).attr("data-actual");
	paging_meta_data.max = $(element).attr("data-max");

	
	// 2. ak je actual > 1, potom aktivuj titleNextIcon
	if (paging_meta_data.actual > 1) {
		$('.titlePrevIcon').attr("style", "cursor:pointer");
		$('.titlePrevIcon').click(function(){
			var url = link + "/" + (parseInt(paging_meta_data.actual) - 1);
			$.get(url, {}, function(e) {
                $(".inner").html(e);
                paging_init(element, link);
            });
		});
	}
	// 3. ak je actual < max, potom aktivuj titlePrevIcon
	if (paging_meta_data.actual < paging_meta_data.max) {
		$('.titleNextIcon').attr("style", "cursor:pointer");
		$('.titleNextIcon').click(function(){
			var url = link + "/" + (parseInt(paging_meta_data.actual) + 1);
			$.get(url, {}, function(e) {
                $(".inner").html(e);
                paging_init(element, link);
            });
		});
	}
	// that's all folks
}