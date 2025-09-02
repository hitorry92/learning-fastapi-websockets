# learning-fastapi-websockets
This project is a simple, real-time chat application built to understand the fundamentals of FastAPI and WebSockets. The goal is to learn how to handle bidirectional communication between a server and multiple clients, a key concept for building real-time services.

### 1단계: 프로젝트 기본 설정

먼저 프로젝트를 위한 가상 환경을 만들고 필요한 패키지를 설치해야 합니다.

- **FastAPI 설치**: `uv add fastapi uvicorn websockets`
    
- **WebSockets 라이브러리 설치**: FastAPI는 웹소켓을 지원하므로 별도의 라이브러리 없이 구현 가능하지만, 일반적으로 클라이언트와 서버 간의 통신을 위해 `websockets` 라이브러리를 함께 사용하거나 프레임워크가 제공하는 기능을 활용합니다. FastAPI는 내부적으로 **Starlette** 라이브러리를 사용하며, 웹소켓 기능은 이미 포함되어 있습니다.
    
- **클라이언트 측**: 간단한 HTML/JavaScript 파일을 작성하여 웹소켓 연결을 시도하고 메시지를 주고받는 기능을 구현합니다.
    

---

### 2단계: 백엔드(FastAPI) 구현

FastAPI를 사용해 웹소켓 서버를 구축합니다.

1. **메인 파일 생성**: `main.py` 파일을 만들고 FastAPI 애플리케이션을 초기화합니다.
    
2. **웹소켓 라우트 정의**: `@app.websocket("/ws")` 데코레이터를 사용해 웹소켓 연결을 처리할 엔드포인트를 만듭니다. 이 라우트는 클라이언트가 연결을 요청하는 경로가 됩니다.
    
3. **연결 관리**: 여러 클라이언트가 동시에 접속할 수 있으므로, 연결된 클라이언트들을 관리하는 리스트나 집합(Set)을 만들어야 합니다. 새로운 클라이언트가 연결되면 리스트에 추가하고, 연결이 끊기면 제거하는 로직을 구현합니다.
    
4. **메시지 수신 및 전송**: 웹소켓 연결이 확립되면, `await websocket.receive_text()`를 이용해 클라이언트로부터 메시지를 받습니다. 메시지를 받은 후에는 모든 연결된 클라이언트들에게 `await connection.send_text(message)`를 이용해 받은 메시지를 다시 전송하는 로직을 작성합니다.
    

---

### 3단계: 프론트엔드(HTML/JavaScript) 구현

사용자 인터페이스를 만들어 백엔드와 통신합니다.

1. **HTML 파일 생성**: 메시지를 입력할 텍스트 상자, 전송 버튼, 그리고 채팅 기록을 보여줄 영역이 포함된 `index.html` 파일을 만듭니다.
    
2. **JavaScript 코드 작성**:
    
    - `WebSocket` 객체를 생성하여 백엔드의 웹소켓 URL(`ws://localhost:8000/ws`)에 연결합니다.
        
    - `ws.onopen`, `ws.onmessage`, `ws.onclose`, `ws.onerror` 같은 이벤트 핸들러를 사용하여 연결 상태를 관리하고 서버로부터 받은 메시지를 화면에 표시합니다.
        
    - 사용자가 메시지를 입력하고 전송 버튼을 누르면 `ws.send()` 메서드를 이용해 메시지를 백엔드로 보냅니다.
        

---

### 4단계: 테스트 및 실행

개발한 애플리케이션을 실행하고 테스트합니다.

- **백엔드 실행**: 터미널에서 `uvicorn main:app --reload` 명령어를 실행하여 FastAPI 서버를 시작합니다. `--reload` 옵션은 코드가 변경될 때마다 서버를 자동으로 재시작해줘서 개발 편의성을 높여줍니다.
    
- **프론트엔드 실행**: 웹 브라우저에서 `index.html` 파일을 열거나, 간단한 웹 서버(예: Python의 `http.server`)를 이용해 파일을 띄웁니다.
    
- **실시간 테스트**: 두 개 이상의 브라우저 탭을 열고 각기 다른 메시지를 입력해보며 실시간으로 메시지가 공유되는지 확인합니다. 이 과정에서 웹소켓이 어떻게 양방향 통신을 가능하게 하는지 직접 경험할 수 있습니다.