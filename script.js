async function loginStudent() {

    const roll = document.getElementById("roll").value;
    const branch = document.getElementById("branch").value;
    const year = document.getElementById("year").value;

    const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            roll: roll,
            branch: branch,
            year: year
        })
    });

    const data = await response.json();

    if (data.status === "success") {
    window.location.href = "dashboard.html";

}

 else {
        alert("Student Not Found ❌");
    }
}

