<template>
    <div class="mb-5">
      <nav id="header"
           class="navbar navbar-expand-lg navbar-dark nav-pills bg-primary">
        <a class="navbar-brand mb-0 h1" href="/">WebDownloader</a>
        <button class="navbar-toggler"
                type="button"
                data-toggle="collapse"
                data-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent"
                aria-expanded="false"
                aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
  <!--            active if site==title-->
              <a class="nav-link" href="/">Home <span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item active">
              <a class="nav-link" href="tasks">Task list</a>
            </li>
          </ul>

        </div>
      </nav>
    </div>
</template>

<script>
export default {
  name: 'Header',
};
</script>
