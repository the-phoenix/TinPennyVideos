import React, { PureComponent, Fragment } from "react"
import { Field, reduxForm } from "redux-form"
import classNames from 'classnames'

import {email, required} from '../validators';

const renderField = ({
  type,
  label,
  name,
  input,
  meta: { touched, error, warning }, // eslint-disable-line
  serverError,
  leftIcon,
  ...props
}) => {
  const hasError = (touched && (error || warning)) || serverError

  return (
    <div className="field">
      <label className="label has-text-black">{label}</label>
      <div className="control has-icons-left has-icons-right">
        <input 
          type={type}
          className={classNames("input", {
            "is-danger": hasError
          })}
          {...input}
          placeholder={`Enter ${label}`}
        />
        {leftIcon && <span className="icon is-small is-left">
          <i className={`fa fa-${leftIcon}`}></i>
        </span>}
        {hasError && [
          <span className="icon is-small is-right" key={`${name}-error-icon`}>
            <i className="fa fa-exclamation-triangle"></i>
          </span>,
          (error && <p className="help is-danger" key={`${name}-client-val-error`}>{error}</p>) ||
            (warning && <p className="help is-warning" key={`${name}-client-val-warning`}>{warning}</p>),
          serverError && serverError.length && 
            serverError.map((e, idx) => <p className="help is-danger" key={`${name}-server-val-error-${idx}`}>{e}</p>)
        ]}
      </div>
    </div>
  )
};

const LoginForm = props => { 
  const { handleSubmit, serverError, submitting } = props;

  let nonFieldWarning;
  if (serverError && serverError.non_field_errors) {
    nonFieldWarning = serverError.non_field_errors.join("\n");
  }

  return (
    <Fragment>
      <h3 className="title">Login</h3>
      <hr className="login-hr" />
      {nonFieldWarning && <p className="subtitle has-text-danger">{nonFieldWarning}</p>}
      {!nonFieldWarning && <p className="subtitle">Please login to proceed.</p>}
      <div className="box has-background-white">
        <form layout="vertical" onSubmit={handleSubmit} noValidate>
          <Field
            name="email"
            label="Email"
            type="email"
            component={renderField}
            serverError={serverError && serverError['email']}
            validate={[required, email]}
            leftIcon="envelope"
          />
          <Field
            name="password"
            label="Password"
            type="password"
            component={renderField}
            serverError={serverError && serverError['password']}
            validate={[required]}
            leftIcon="lock"
          />
          <div className="field">&nbsp;</div>
          <button className="button is-block is-info is-large is-fullwidth" disabled={submitting}>
            Login <i className="fa fa-sign-in" aria-hidden="true"></i>
          </button>
        </form>
      </div>
    </Fragment>
  );
}

export default reduxForm({ 
  form: "login" 
})(LoginForm)
