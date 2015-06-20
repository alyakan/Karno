       $(document).ready(function(){
            $('input[type="checkbox"][name="group"').on('change', function(){
                if(this.checked){
                    $('div#hidden').removeClass("hidden");
                }
                else {
                    $('div#hidden').addClass("hidden");
                }
            });

            $('input[type="checkbox"][name="public"').on('change', function(){
                if(this.checked){
                    $('div#hidden').addClass("hidden");
                }
            });

            $('input[type="checkbox"][name="registered_users"').on('change', function(){
                if(this.checked){
                    $('div#hidden').addClass("hidden");
                }
            });
        });