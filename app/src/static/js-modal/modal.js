document.getElementById("btnInstrucoes").addEventListener("click", function() {
    document.getElementById("modalInstrucoes").classList.remove("hidden");
  });
  
  document.getElementById("fecharModal").addEventListener("click", function() {
    document.getElementById("modalInstrucoes").classList.add("hidden");
  });
  
  // Fecha o modal se clicar fora do conteúdo
  window.addEventListener("click", function(event) {
    const modal = document.getElementById("modalInstrucoes");
    if (event.target === modal) {
      modal.classList.add("hidden");
    }
  });