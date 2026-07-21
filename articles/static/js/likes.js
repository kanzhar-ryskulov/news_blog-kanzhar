document.addEventListener("DOMContentLoaded", function () {

    let buttons = document.querySelectorAll(".like-button");

    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener("click", likeButtonClicked);
    }

    function likeButtonClicked(event) {
        const button = event.currentTarget;

        const type = button.getAttribute("data-type");
        const id = button.getAttribute("data-id");
        let likedNow = button.getAttribute("data-liked");

        let url = "";
        let method = "";

        if (likedNow === "1") {
            url = "/" + type + "/" + id + "/unlike/";
            method = "DELETE";
        } else {
            url = "/" + type + "/" + id + "/like/";
            method = "POST";
        }

        let csrftoken = getCookieValue("csrftoken");

        fetch(url, {
            method: method,
            headers: {
                "X-CSRFToken": csrftoken
            }
        }).then(function (response) {
            return response.json();
        }).then(function (data) {
            updateButton(button, data.liked, data.likes_count);
        });
    }

    function updateButton(button, liked, likesCount) {
        if (liked === true) {
            button.setAttribute("data-liked", "1");
            button.querySelector(".like-text").innerHTML = "Анлайк";
        } else {
            button.setAttribute("data-liked", "0");
            button.querySelector(".like-text").innerHTML = "Лайк";
        }

        button.querySelector(".like-count").innerHTML = likesCount;

        let icon = button.querySelector(".like-icon");
        if (icon) {
            if (liked === true) {
                icon.classList.remove("fa-regular");
                icon.classList.add("fa-solid");
            } else {
                icon.classList.remove("fa-solid");
                icon.classList.add("fa-regular");
            }
        }
    }

    function getCookieValue(name) {
        let allCookies = document.cookie;
        let cookiesArray = allCookies.split("; ");

        for (let i = 0; i < cookiesArray.length; i++) {
            let oneCookie = cookiesArray[i].split("=");
            if (oneCookie[0] === name) {
                return oneCookie[1];
            }
        }
        return null;
    }

});
