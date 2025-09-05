// import


/* class redirecting */
export class Redirecting {

    constructor(domain, redirect, flag) {
        this.domain = domain;
        this.redirect = redirect;
        this.flag = flag;

        this.initEventRedirecting();
    }

    initEventRedirecting() {
        this.redirectingUrlPage();
    }

    redirectingUrlPage() {
        setTimeout(() => {
            window.location.href = `http://127.0.0.1:8000/${this.domain}/${this.redirect}?fg=${this.flag}`;
        }, 1200);
    }

}