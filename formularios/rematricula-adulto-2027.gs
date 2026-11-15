/**
 * Barro na Veia – Escola de Cerâmica
 * Cria o "Formulário de Rematrícula 2027 – Adulto" no Google Formulários.
 *
 * COMO USAR (logado na conta Google do Barro na Veia):
 * 1. Acesse https://script.google.com e clique em "Novo projeto".
 * 2. Apague o conteúdo que aparece e cole este arquivo inteiro.
 * 3. Preencha PRAZO e HORARIOS logo abaixo (opcional; dá para ajustar depois no Formulários).
 * 4. Clique em "Executar" (função criarFormularioRematriculaAdulto2027) e autorize o acesso.
 * 5. Veja os links em "Registro de execução". O formulário também aparece no Google Drive.
 */

// ===== AJUSTES DA SECRETARIA =====

// Prazo de envio. Deixe '' se ainda não estiver definido.
var PRAZO = '';

// Dias e horários das turmas 2027. Ex.: ['Terça, 9h às 12h', 'Quinta, 14h às 17h']
// Se ficar vazio, a pergunta 3.2 vira resposta curta.
var HORARIOS = [];

// Pergunta 5.4 (autorização de imagens das peças): true para incluir, false para retirar.
var INCLUIR_AUTORIZACAO_IMAGEM = true;

// =================================

function criarFormularioRematriculaAdulto2027() {
  var form = FormApp.create('Rematrícula 2027 – Adulto | Barro na Veia');

  var prazoTexto = PRAZO ? 'Prazo para envio: ' + PRAZO + '.' : 'Prazo para envio: [a definir].';

  form.setDescription(
    'Que alegria seguir mais um ano com você no ateliê! Em 2027, continuamos abrindo espaço ' +
    'para seus projetos, suas pesquisas e suas descobertas no barro, sempre com orientação ' +
    'técnica e artística e no seu ritmo.\n\n' +
    'Preencha este formulário para garantir sua vaga. Leva poucos minutos. ' + prazoTexto + '\n\n' +
    'Criar, experimentar, transformar. Porque, depois que o barro entra na veia, não sai mais!'
  );
  form.setProgressBar(true);
  form.setConfirmationMessage(
    'Obrigada por seguir criando com a gente! Recebemos sua solicitação de rematrícula 2027. ' +
    'Nossa equipe vai analisar e entrar em contato para confirmar sua vaga e formalizar o contrato.\n\n' +
    'Até breve no ateliê, com as mãos no barro.'
  );

  // ---------- Seção 1 – Dados cadastrais ----------
  form.addSectionHeaderItem()
    .setTitle('Seção 1 – Dados cadastrais')
    .setHelpText('Só o necessário para contato e contrato. Confirme ou atualize seus dados.');

  form.addTextItem().setTitle('Nome completo').setRequired(true);
  form.addTextItem().setTitle('CPF').setRequired(true);
  form.addDateItem().setTitle('Data de nascimento').setRequired(false);
  form.addTextItem().setTitle('Celular / WhatsApp').setRequired(true);

  var emailValidacao = FormApp.createTextValidation()
    .setHelpText('Digite um e-mail válido.')
    .requireTextIsEmail()
    .build();
  form.addTextItem().setTitle('E-mail').setRequired(true).setValidation(emailValidacao);

  form.addTextItem().setTitle('Endereço completo (com CEP)').setRequired(true);
  form.addTextItem().setTitle('Contato de emergência (nome e telefone)').setRequired(false);
  form.addMultipleChoiceItem()
    .setTitle('Algum dado mudou desde a última matrícula?')
    .setChoiceValues(['Sim', 'Não'])
    .setRequired(false);

  // ---------- Seção 2 – Carga horária e plano ----------
  form.addPageBreakItem()
    .setTitle('Seção 2 – Carga horária e plano')
    .setHelpText(
      'Valores 2027 – Adulto (por mês e total do plano)\n\n' +
      '3h semanais: Trimestral R$ 740/mês (total R$ 2.220) | Semestral R$ 670/mês (total R$ 4.020) | Anual R$ 590/mês (total R$ 7.080)\n' +
      '4h semanais: Trimestral R$ 940/mês (total R$ 2.820) | Semestral R$ 850/mês (total R$ 5.100) | Anual R$ 750/mês (total R$ 9.000)\n' +
      '5h semanais: Trimestral R$ 1.110/mês (total R$ 3.330) | Semestral R$ 1.005/mês (total R$ 6.030) | Anual R$ 885/mês (total R$ 10.620)\n' +
      '6h semanais: Trimestral R$ 1.260/mês (total R$ 3.780) | Semestral R$ 1.140/mês (total R$ 6.840) | Anual R$ 1.003/mês (total R$ 12.036)\n\n' +
      'No plano anual, a economia frente a 12 meses no valor trimestral é de R$ 1.800 (3h), ' +
      'R$ 2.280 (4h), R$ 2.700 (5h) e R$ 3.084 (6h).\n\n' +
      'Argila e queimas cerâmicas são cobradas à parte. Aulas avulsas são oferecidas apenas pelo aplicativo.'
    );

  form.addMultipleChoiceItem()
    .setTitle('Qual carga horária semanal você deseja em 2027?')
    .setChoiceValues(['3h semanais', '4h semanais', '5h semanais', '6h semanais'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Qual plano você escolhe?')
    .setChoiceValues(['Trimestral (3 parcelas)', 'Semestral (6 parcelas)', 'Anual (12 parcelas)'])
    .setRequired(true);

  // ---------- Seção 3 – Turma e horário ----------
  form.addPageBreakItem()
    .setTitle('Seção 3 – Turma e horário')
    .setHelpText('A vaga no horário escolhido depende de disponibilidade e da aprovação do ateliê.');

  form.addMultipleChoiceItem()
    .setTitle('Deseja manter sua turma e horário atuais?')
    .setChoiceValues(['Sim', 'Não, quero mudar'])
    .setRequired(true);

  if (HORARIOS.length > 0) {
    form.addCheckboxItem()
      .setTitle('Se quiser mudar, quais horários funcionam para você?')
      .setChoiceValues(HORARIOS)
      .setRequired(false);
  } else {
    form.addTextItem()
      .setTitle('Se quiser mudar, quais dias e horários funcionam para você?')
      .setRequired(false);
  }

  form.addParagraphTextItem()
    .setTitle('Quer contar algo sobre seus projetos ou interesses para 2027?')
    .setRequired(false);

  // ---------- Seção 4 – Informações importantes + Seção 5 – Declaração ----------
  form.addPageBreakItem()
    .setTitle('Informações importantes e declaração')
    .setHelpText(
      '• Materiais: argila e queimas cerâmicas são cobradas separadamente da mensalidade.\n' +
      '• Reposições: você pode antecipar ou repor até duas aulas por mês, com agendamento e conforme ' +
      'disponibilidade. Casos de doença ou falecimento de familiares podem ser analisados individualmente.\n' +
      '• Viagens e férias: viagens e férias particulares não suspendem automaticamente as mensalidades.\n' +
      '• Trancamento: opcional, por até 60 dias por ano, com taxa de reserva de vaga de 50% da ' +
      'mensalidade, conforme as condições do contrato.\n' +
      '• Fidelidade: os descontos dos planos semestral e anual estão vinculados à duração contratada, ' +
      'respeitadas as condições legais de cancelamento.\n' +
      '• Confirmação: a rematrícula só é confirmada após aprovação do ateliê e formalização das ' +
      'condições contratuais.'
    );

  form.addCheckboxItem()
    .setTitle('Li e estou de acordo com as informações sobre materiais, reposições, trancamento e fidelidade.')
    .setChoiceValues(['Li e concordo'])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('Estou ciente de que a rematrícula só é confirmada após aprovação do ateliê e formalização do contrato.')
    .setChoiceValues(['Estou ciente'])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('Autorizo o uso dos meus dados para contato e gestão da minha matrícula.')
    .setChoiceValues(['Autorizo'])
    .setRequired(true);

  if (INCLUIR_AUTORIZACAO_IMAGEM) {
    form.addMultipleChoiceItem()
      .setTitle('Autorizo o uso de imagens das minhas peças nas redes sociais do Barro na Veia.')
      .setChoiceValues(['Sim', 'Não'])
      .setRequired(false);
  }

  Logger.log('Formulário criado!');
  Logger.log('Link para EDITAR: ' + form.getEditUrl());
  Logger.log('Link para os ALUNOS responderem: ' + form.getPublishedUrl());
}
