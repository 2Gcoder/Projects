let UserScore = 0;
let CompScore = 0;
let userscorePara = document.querySelector("#user-score");
let compscorePara = document.querySelector("#comp-score");
let msg = document.querySelector("#mssg");

let choices = document.querySelectorAll(".choice");

const ShowWinner = (userwin,user_choice,comp_choice) => {
    if (userwin) {
        msg.innerText = `YOU WIN ! ${user_choice} beats ${comp_choice} `;
        msg.style.color = "aliceblue";
        msg.style.backgroundColor = "green";
        UserScore++;
        userscorePara.innerText = UserScore;
    } else {
        msg.innerText = `YOU LOSE !  ${comp_choice} beats ${user_choice}`;
        msg.style.color = "aliceblue";
        msg.style.backgroundColor = "red";
        CompScore++;
        compscorePara.innerText = CompScore;
    }
};

const drawgame = () => {
    msg.innerText = "DRAW";
    msg.style.color = "aliceblue";
        msg.style.backgroundColor = "#081b31";
};

choices.forEach((choice) => {
    choice.addEventListener("click", () => {
        const userchoice = choice.getAttribute("id");
        playgame(userchoice);
    });
});

const playgame = (user_choice) => {
    console.log("user_choice: ", user_choice);
    const comp_choice = gencompchoice();
    console.log("comp_choice : ", comp_choice);

    let userwin = true;

    if (user_choice === comp_choice) {
        drawgame();
        return;
    } else {
        if (user_choice === "rock")
            userwin = comp_choice === "paper" ? false : true;
        else {
            if (user_choice === "paper")
                userwin = comp_choice === "scissors" ? false : true;
            else {
                if (user_choice === "scissors")
                    userwin = comp_choice === "rock" ? false : true;
            }
        }
    }

    ShowWinner(userwin,user_choice,comp_choice);
};

const gencompchoice = () => {
    const option = ["paper", "rock", "scissors"];
    const randidx = Math.floor(Math.random() * 3);
    return option[randidx];
};