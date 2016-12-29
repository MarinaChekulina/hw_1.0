jQuery(function () {

  var $feed = $(".feed"),
    $trigger = $(".next_page"),
    $spinner = $(".spinner"),
    spinner = "<div class=\"spinner\"></div>";

  var isotopeSettings = {
    itemSelector: ".box"
  }

  $trigger.on("click", function (e) {
    e.preventDefault();

    var $this = $(this),
      originalURL = $(this).attr("href");

    // Get url variables and return an object
    function getUrlVars() {

      var vars = {}, hash;
      var hashes = originalURL.slice(originalURL.indexOf("?") + 1).split("&");

      for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split("=");
        vars[hash[0]] = hash[1];
      }

      return vars;

    }

    // Construct new url
    function newURL() {

      var urlVars = getUrlVars();
        urlVars["page"] = parseInt(urlVars["page"]) + 1;

      var newParams = $.map(urlVars, function(value, key) {
        return key + "=" + value;
      }).join("&");

      return originalURL.substring(0, originalURL.lastIndexOf("?")) + "?" + newParams;

    }

    // load all post divs from page 2 into an off-DOM div
    $("<div/>").load(originalURL + ".box", function () {

      var $temp = $(this),
        newElements = $temp.contents();

      // Show spinner
      $this.hide().after(spinner);

      if (newElements.length !== 0) {
        // Wait a bit so that the images load
        // (this is here just to demonstrate the loading, not a real fix)
        setTimeout(function () {

          // once they're loaded append to content area
          $(newElements)
            .appendTo($feed)
            .hide();

          // Change href & relayout new items
          $this.attr("href", newURL());
          $feed.isotope("appended", $(newElements), function () {
            $(newElements).fadeIn();
          });

          // Hide spinner & Fade in load more button
          $spinner.fadeOut().remove();
          $this.fadeIn();

        }, 600);
      } else {
        // In case there no more content to load:
        $this.replaceWith("<span>You've reached the end of the web.</span>");
        $spinner.fadeOut().remove();
        $this.fadeIn();
      }
    });

  });

});
