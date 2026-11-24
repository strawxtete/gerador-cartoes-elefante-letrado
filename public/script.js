const estado = {
    temaEscuro: true,
    turmaNome: "turma",
    alunos: [],
    urlPdfLote: null,
    urlPdfManual: null
};

const btnTema = document.getElementById("btn-tema");
const botoesAba = document.querySelectorAll(".aba-btn");
const conteudosAba = document.querySelectorAll(".aba-conteudo");

const dropzone = document.getElementById("dropzone");
const inputPdf = document.getElementById("input-pdf");
const btnProcurar = document.getElementById("btn-procurar");
const arquivoBox = document.getElementById("arquivo-selecionado");
const arquivoNome = document.getElementById("arquivo-nome");
const arquivoTamanho = document.getElementById("arquivo-tamanho");
const btnRemoverArquivo = document.getElementById("btn-remover-arquivo");

const alertaPdf = document.getElementById("alerta-pdf");
const avisoPdf = document.getElementById("aviso-pdf");
const secaoTabela = document.getElementById("secao-tabela");
const tbodyAlunos = document.getElementById("tbody-alunos");
const btnAdicionarLinha = document.getElementById("btn-adicionar-linha");
const btnGerarLote = document.getElementById("btn-gerar-lote");
const progressoLote = document.getElementById("progresso-lote");
const progressoLoteTexto = document.getElementById("progresso-lote-texto");
const progressoLoteBarra = document.getElementById("progresso-lote-preenchimento");
const resultadoLote = document.getElementById("resultado-lote");
const badgeLote = document.getElementById("badge-lote");
const btnBaixarLote = document.getElementById("btn-baixar-lote");

const inputManualNome = document.getElementById("manual-nome");
const inputManualSenha = document.getElementById("manual-senha");
const alertaManual = document.getElementById("alerta-manual");
const btnGerarManual = document.getElementById("btn-gerar-manual");
const progressoManual = document.getElementById("progresso-manual");
const progressoManualBarra = document.getElementById("progresso-manual-preenchimento");
const resultadoManual = document.getElementById("resultado-manual");
const badgeManual = document.getElementById("badge-manual");
const btnBaixarManual = document.getElementById("btn-baixar-manual");

btnTema.addEventListener("click", () => {
    estado.temaEscuro = !estado.temaEscuro;
    document.body.className = estado.temaEscuro ? "tema-escuro" : "tema-claro";
    btnTema.textContent = estado.temaEscuro ? "Modo Claro" : "Modo Escuro";
});

botoesAba.forEach((botao) => {
    botao.addEventListener("click", () => {
        const alvo = botao.getAttribute("data-aba");
        botoesAba.forEach((b) => {
            b.classList.remove("ativa");
            b.setAttribute("aria-selected", "false");
        });
        conteudosAba.forEach((c) => c.classList.remove("ativa"));
        botao.classList.add("ativa");
        botao.setAttribute("aria-selected", "true");
        document.getElementById(alvo).classList.add("ativa");
    });
});

function formatarTamanho(bytes) {
    if (bytes < 1024) return `${bytes} B`;
    const kb = bytes / 1024;
    if (kb < 1024) return `${kb.toFixed(1)} KB`;
    return `${(kb / 1024).toFixed(2)} MB`;
}

function limparNomeArquivo(texto, padrao = "cartoes") {
    const limpo = texto.replace(/[\\/*?:"<>|]+/g, "").trim().replace(/\s+/g, " ");
    return limpo || padrao;
}

function mostrarAlerta(elemento, mensagem, tipo) {
    elemento.textContent = mensagem;
    elemento.className = `alerta alerta-${tipo}`;
}

function ocultarElemento(elemento) {
    elemento.classList.add("oculto");
}

function mostrarElemento(elemento) {
    elemento.classList.remove("oculto");
}

function resetarEstadoPdf() {
    inputPdf.value = "";
    estado.alunos = [];
    estado.turmaNome = "turma";
    if (estado.urlPdfLote) {
        URL.revokeObjectURL(estado.urlPdfLote);
        estado.urlPdfLote = null;
    }
    ocultarElemento(arquivoBox);
    ocultarElemento(alertaPdf);
    ocultarElemento(avisoPdf);
    ocultarElemento(secaoTabela);
    ocultarElemento(progressoLote);
    ocultarElemento(resultadoLote);
    tbodyAlunos.innerHTML = "";
    btnGerarLote.disabled = true;
}

function renderizarTabela() {
    tbodyAlunos.innerHTML = "";
    estado.alunos.forEach((aluno, idx) => {
        const tr = document.createElement("tr");

        const tdNome = document.createElement("td");
        const inpNome = document.createElement("input");
        inpNome.type = "text";
        inpNome.value = aluno.nome;
        inpNome.placeholder = "Nome do aluno";
        inpNome.addEventListener("input", (e) => {
            estado.alunos[idx].nome = e.target.value;
            ocultarElemento(resultadoLote);
        });
        tdNome.appendChild(inpNome);

        const tdSenha = document.createElement("td");
        const inpSenha = document.createElement("input");
        inpSenha.type = "text";
        inpSenha.value = aluno.senha;
        inpSenha.placeholder = "Senha";
        inpSenha.addEventListener("input", (e) => {
            estado.alunos[idx].senha = e.target.value;
            ocultarElemento(resultadoLote);
        });
        tdSenha.appendChild(inpSenha);

        const tdAcao = document.createElement("td");
        const btnRem = document.createElement("button");
        btnRem.type = "button";
        btnRem.className = "btn-texto-remover";
        btnRem.textContent = "Remover";
        btnRem.addEventListener("click", () => {
            estado.alunos.splice(idx, 1);
            renderizarTabela();
            ocultarElemento(resultadoLote);
            btnGerarLote.disabled = estado.alunos.length === 0;
        });
        tdAcao.appendChild(btnRem);

        tr.appendChild(tdNome);
        tr.appendChild(tdSenha);
        tr.appendChild(tdAcao);
        tbodyAlunos.appendChild(tr);
    });
    btnGerarLote.disabled = estado.alunos.length === 0;
}

btnAdicionarLinha.addEventListener("click", () => {
    estado.alunos.push({ nome: "", senha: "" });
    renderizarTabela();
    ocultarElemento(resultadoLote);
    const inputs = tbodyAlunos.querySelectorAll("tr:last-child input");
    if (inputs.length > 0) inputs[0].focus();
});

btnProcurar.addEventListener("click", (e) => {
    e.stopPropagation();
    inputPdf.click();
});

dropzone.addEventListener("click", () => {
    inputPdf.click();
});

dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("arrastando");
});

dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("arrastando");
});

dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("arrastando");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        processarArquivoPdf(e.dataTransfer.files[0]);
    }
});

inputPdf.addEventListener("change", () => {
    if (inputPdf.files && inputPdf.files.length > 0) {
        processarArquivoPdf(inputPdf.files[0]);
    }
});

btnRemoverArquivo.addEventListener("click", () => {
    resetarEstadoPdf();
});

async function processarArquivoPdf(arquivo) {
    resetarEstadoPdf();

    arquivoNome.textContent = arquivo.name;
    arquivoTamanho.textContent = formatarTamanho(arquivo.size);
    mostrarElemento(arquivoBox);

    if (!arquivo.name.toLowerCase().endsWith(".pdf")) {
        mostrarAlerta(alertaPdf, "Formato inválido. Selecione um arquivo PDF.", "erro");
        return;
    }

    const formData = new FormData();
    formData.append("arquivo", arquivo);

    try {
        const resp = await fetch("/api/extrair", {
            method: "POST",
            body: formData
        });
        const dados = await resp.json();
        if (!resp.ok) {
            mostrarAlerta(alertaPdf, dados.detail || "Não foi possível ler o PDF.", "erro");
            return;
        }

        estado.alunos = dados.alunos || [];
        estado.turmaNome = dados.turma || "turma";

        if (estado.alunos.length === 0) {
            mostrarAlerta(
                alertaPdf,
                "Nenhum aluno encontrado. Verifique se o PDF segue o padrão esperado.",
                "erro"
            );
            return;
        }

        mostrarAlerta(alertaPdf, `${estado.alunos.length} alunos encontrados.`, "sucesso");

        if (dados.esperado !== null && dados.esperado !== undefined && dados.esperado !== estado.alunos.length) {
            mostrarAlerta(
                avisoPdf,
                `O cabeçalho do PDF indica ${dados.esperado} alunos, mas foram lidos ${estado.alunos.length}. Confira a lista abaixo.`,
                "aviso"
            );
        }

        renderizarTabela();
        mostrarElemento(secaoTabela);
    } catch (erro) {
        mostrarAlerta(alertaPdf, "Erro ao comunicar com o servidor para ler o PDF.", "erro");
    }
}

btnGerarLote.addEventListener("click", async () => {
    const validos = estado.alunos.filter(
        (a) => a.nome && a.nome.trim() !== "" && a.senha && a.senha.trim() !== ""
    );

    if (validos.length === 0) {
        mostrarAlerta(alertaPdf, "A lista está vazia. Preencha ao menos um aluno.", "erro");
        return;
    }

    ocultarElemento(resultadoLote);
    mostrarElemento(progressoLote);
    btnGerarLote.disabled = true;

    let progressoAtual = 15;
    progressoLoteBarra.style.width = `${progressoAtual}%`;
    progressoLoteTexto.textContent = `Gerando cartões... 0/${validos.length}`;

    const intervalo = setInterval(() => {
        if (progressoAtual < 90) {
            progressoAtual += 10;
            const estimativa = Math.min(
                validos.length,
                Math.max(1, Math.round((progressoAtual / 100) * validos.length))
            );
            progressoLoteBarra.style.width = `${progressoAtual}%`;
            progressoLoteTexto.textContent = `Gerando cartões... ${estimativa}/${validos.length}`;
        }
    }, 180);

    try {
        const nomeLimpo = limparNomeArquivo(estado.turmaNome, "turma");
        const resp = await fetch("/api/gerar-pdf", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                alunos: validos,
                nome_arquivo: nomeLimpo
            })
        });

        clearInterval(intervalo);

        if (!resp.ok) {
            let msg = "Erro ao gerar os cartões.";
            try {
                const err = await resp.json();
                if (err.detail) msg = err.detail;
            } catch (_) {}
            ocultarElemento(progressoLote);
            mostrarAlerta(alertaPdf, msg, "erro");
            btnGerarLote.disabled = false;
            return;
        }

        progressoLoteBarra.style.width = "100%";
        progressoLoteTexto.textContent = `Gerando cartões... ${validos.length}/${validos.length}`;

        const blob = await resp.blob();
        if (estado.urlPdfLote) URL.revokeObjectURL(estado.urlPdfLote);
        estado.urlPdfLote = URL.createObjectURL(blob);

        const qtd = validos.length;
        const paginas = Math.ceil(qtd / 6);
        const labelPag = paginas === 1 ? "folha A4" : "folhas A4";

        badgeLote.textContent = `${qtd} cartões gerados • ${paginas} ${labelPag} para impressão`;
        btnBaixarLote.href = estado.urlPdfLote;
        btnBaixarLote.download = `${nomeLimpo}.pdf`;

        ocultarElemento(progressoLote);
        mostrarElemento(resultadoLote);
    } catch (erro) {
        clearInterval(intervalo);
        ocultarElemento(progressoLote);
        mostrarAlerta(alertaPdf, "Erro de conexão ao gerar os cartões.", "erro");
    } finally {
        btnGerarLote.disabled = false;
    }
});

btnGerarManual.addEventListener("click", async () => {
    const nome = inputManualNome.value.trim();
    const senha = inputManualSenha.value.trim();

    ocultarElemento(alertaManual);
    ocultarElemento(resultadoManual);

    if (!nome || !senha) {
        mostrarAlerta(alertaManual, "Preencha o nome e a senha do aluno.", "erro");
        return;
    }

    mostrarElemento(progressoManual);
    progressoManualBarra.style.width = "45%";
    btnGerarManual.disabled = true;

    try {
        const nomeLimpo = limparNomeArquivo(nome, "aluno");
        const resp = await fetch("/api/gerar-pdf", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                alunos: [{ nome, senha }],
                nome_arquivo: nomeLimpo
            })
        });

        if (!resp.ok) {
            let msg = "Erro ao gerar o cartão.";
            try {
                const err = await resp.json();
                if (err.detail) msg = err.detail;
            } catch (_) {}
            ocultarElemento(progressoManual);
            mostrarAlerta(alertaManual, msg, "erro");
            btnGerarManual.disabled = false;
            return;
        }

        progressoManualBarra.style.width = "100%";
        const blob = await resp.blob();
        if (estado.urlPdfManual) URL.revokeObjectURL(estado.urlPdfManual);
        estado.urlPdfManual = URL.createObjectURL(blob);

        badgeManual.textContent = `Cartão gerado para ${nomeLimpo}`;
        btnBaixarManual.href = estado.urlPdfManual;
        btnBaixarManual.download = `${nomeLimpo}.pdf`;

        ocultarElemento(progressoManual);
        mostrarElemento(resultadoManual);
    } catch (erro) {
        ocultarElemento(progressoManual);
        mostrarAlerta(alertaManual, "Erro de conexão ao gerar o cartão.", "erro");
    } finally {
        btnGerarManual.disabled = false;
    }
});
