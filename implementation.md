# MLOps Implementation and Architecture

Based on the project described in your workspace (Decision Tree Classifier with Docker, GitHub Actions, and Kubernetes), below is the optimal architecture design and a set of tough viva questions.

## 1. Architecture Design

The following Mermaid diagram illustrates the end-to-end MLOps architecture, highlighting the flow from local development to a scalable production deployment.

```mermaid
graph TD
    %% Local Environment
    subgraph Local["Local Development Environment"]
        Dev((Developer))
        Code[Source Code<br/>train.py, app.py]
        Dev --> |Writes| Code
    end

    %% Version Control
    subgraph VCS["Version Control System"]
        GitHub[GitHub Repository<br/>dev / docker_cicd]
        Code --> |Git Push| GitHub
    end

    %% Continuous Integration
    subgraph CI["Continuous Integration (GitHub Actions)"]
        Workflow[CI Workflow<br/>.github/workflows/ci.yml]
        GitHub --> |Triggers| Workflow
        Workflow --> |1. Setup Python| Env[Environment Setup]
        Env --> |2. Train Model| Train[train.py]
        Train --> |3. Test Model| Test[test.py]
    end

    %% Containerization
    subgraph Containerization["Containerization & Registry"]
        DockerBuild[Docker Build]
        DockerHub[(Docker Hub<br/>iitj1058/decisiontreeclassifier:v1)]
        Workflow -.-> |Future Enhancement: Auto-build| DockerBuild
        DockerBuild --> |Docker Push| DockerHub
    end

    %% Orchestration
    subgraph Orchestration["Kubernetes Cluster"]
        Deployment[K8s Deployment<br/>replicas: 3]
        Pod1[Pod 1: Flask App]
        Pod2[Pod 2: Flask App]
        Pod3[Pod 3: Flask App]
        Service[K8s Service<br/>Type: NodePort]
        
        DockerHub --> |Image Pull| Deployment
        Deployment --> Pod1
        Deployment --> Pod2
        Deployment --> Pod3
        
        Service --> |Load Balancing| Pod1
        Service --> |Load Balancing| Pod2
        Service --> |Load Balancing| Pod3
    end

    %% End User Access
    subgraph UserAccess["End User"]
        User((End User))
        User --> |HTTP Request: Port 30007| Service
    end
```

## 2. Tough Viva Questions

These questions are designed to test deep understanding of the architecture, design choices, and potential production issues for this MLOps pipeline.

### Machine Learning & Model Selection
1. **Model Choice & Overfitting:** You used a Decision Tree Classifier for the Olivetti Faces dataset. Decision Trees are prone to overfitting, especially on high-dimensional data like images. How did you ensure the model generalized well, and why not use an algorithm more suited for images, like a CNN or even SVM?
2. **Model Serialization Risks:** The model is saved and loaded using `joblib`. What are the security vulnerabilities associated with `joblib` or `pickle` in a production environment, and what safer alternatives exist for model serialization?

### Containerization & Docker
3. **Decoupling Model from Image:** Your Dockerfile likely copies the `savedmodel.pth` directly into the image. What are the architectural drawbacks of baking the model directly into the Docker image, and how would you redesign the system to separate model storage from the application code?
4. **Image Optimization:** The Docker image uses `python:3.11-slim`. While better than the full image, what further steps could you take (e.g., multi-stage builds) to minimize the attack surface and reduce the final image size for deployment?

### CI/CD Pipeline (GitHub Actions)
5. **Pipeline Expansion:** Currently, your GitHub Actions workflow trains and tests the model. If you wanted to fully automate the Docker image build and push to Docker Hub, how would you securely handle the Docker Hub credentials within GitHub, and what security risks must you mitigate?
6. **Data Versioning:** The pipeline relies on downloading the dataset via `scikit-learn` in the code. How would you handle a scenario where the training dataset needs to be updated frequently? What tools (e.g., DVC) would you integrate into this CI/CD pipeline to manage data versioning?

### Kubernetes Orchestration
7. **Service Exposure:** You exposed the application using a `NodePort` service. In an enterprise production environment, why is `NodePort` generally discouraged, and what are the benefits of using a `LoadBalancer` or an `Ingress` controller instead?
8. **Statelessness and Scaling:** Kubernetes is maintaining 3 replicas of your Flask app. Is your application strictly stateless? If an end-user uploads an image, and the request is distributed among the 3 pods, how does the system ensure the request is processed correctly without session persistence issues?
9. **Self-healing vs. Application Errors:** You demonstrated that deleting a pod causes Kubernetes to recreate it. However, if your Flask app starts throwing `500 Internal Server Error` due to a missing dependency, Kubernetes might not automatically restart the pod. How would you configure `liveness` and `readiness` probes to ensure Kubernetes can detect and handle application-level failures?

### Monitoring & Operations
10. **Model Drift:** The model is deployed and serving predictions. How would you monitor the model's predictive performance over time in this architecture to detect data drift (e.g., users uploading images quite different from the Olivetti faces)? What metrics would you expose and collect?
