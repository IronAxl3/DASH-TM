document.getElementById("btn-calcular").onclick = function () {
    this.innerHTML = "💪 Calculando...";
    setTimeout(() => this.innerHTML = "✅ Listo", 1200);
};