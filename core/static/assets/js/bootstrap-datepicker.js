/*
 * Copyright (c) 2021-2021.
 * Julio Cezar Riffel<julioriffel@gmail.com>
 */

//
// Bootstrap Datepicker
//

'use strict';

var Datepicker = (function () {

    // Variables

    var $datepicker = $('.datepicker');


    // Methods

    function init($this) {
        var options = {
            disableTouchKeyboard: true,
            autoclose: false
        };

        $this.datepicker(options);
    }


    // Events

    if ($datepicker.length) {
        $datepicker.each(function () {
            init($(this));
        });
    }

})();
