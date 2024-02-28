let currentSlide = 0;
      const intervalTime = 5000; // 5 seconds
    
      function showSlide(index) {
        const slides = document.querySelector('.slides');
        const slideWidth = document.querySelector('.slide').offsetWidth;
    
        if (index >= slides.children.length) {
          currentSlide = 0;
        } else if (index < 0) {
          currentSlide = slides.children.length - 1;
        } else {
          currentSlide = index;
        }
    
        slides.style.transform = `translateX(${-currentSlide * slideWidth}px)`;
      }
    
      function nextSlide() {
        showSlide(currentSlide + 1);
      }
    
      function prevSlide() {
        showSlide(currentSlide - 1);
      }
    
      setInterval(nextSlide, intervalTime);














